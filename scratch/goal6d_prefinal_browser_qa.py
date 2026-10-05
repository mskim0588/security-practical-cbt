import json
import sys

from playwright.sync_api import sync_playwright


sys.stdout.reconfigure(encoding="utf-8")


BASE_URL = "http://127.0.0.1:5000"
VIEWPORTS = [(360, 740), (390, 844), (430, 932), (1280, 800)]
ROUTES = [
    "/history/68",
    "/result/68",
    "/wrong-notes/Q-SHORT-001",
    "/concepts",
    "/dashboard",
]


def inspect_route(page, path):
    response = page.goto(BASE_URL + path, wait_until="networkidle")
    result = page.evaluate(
        """path => {
          const bodyText = document.body.innerText;
          const result = {
            path,
            status: 0,
            viewportWidth: window.innerWidth,
            documentWidth: document.documentElement.scrollWidth,
            overflow: document.documentElement.scrollWidth > window.innerWidth,
            literalArrowAbsent: !bodyText.includes('&rarr;'),
          };
          if (path.startsWith('/history/')) {
            const explanation = document.querySelector('.explanation-accordion[open] .explanation-body');
            const answerGroups = Array.from(document.querySelectorAll('.accepted-answer-list'));
            const answers = answerGroups.flatMap(group => Array.from(group.querySelectorAll('.accepted-answer-item')));
            const gaps = answerGroups.flatMap(group => {
              const items = Array.from(group.querySelectorAll('.accepted-answer-item'));
              return items.slice(1).map((item, index) =>
                Math.round(item.getBoundingClientRect().top - items[index].getBoundingClientRect().bottom)
              );
            });
            result.history = {
              explanationVisible: Boolean(explanation && explanation.getBoundingClientRect().height > 0),
              rawSourceAbsent: !bodyText.includes('source_type') && !bodyText.includes('total_pages') && !bodyText.includes("{'id': 'SRC-"),
              acceptedAnswerCount: answers.length,
              maxAcceptedAnswerGap: gaps.length ? Math.max(...gaps) : 0,
              aiTriggerVisible: Boolean(document.querySelector('.btn-ai-helper')),
            };
          }
          if (path === '/concepts') {
            const panel = document.querySelector('.concept-filter-panel').getBoundingClientRect();
            const buttonElement = document.querySelector('.search-submit-btn');
            const button = buttonElement.getBoundingClientRect();
            const range = document.createRange();
            range.selectNodeContents(buttonElement);
            const lines = new Set(Array.from(range.getClientRects()).map(rect => Math.round(rect.top)));
            result.concepts = { withinPanel: button.right <= panel.right, searchSingleLine: lines.size === 1 };
          }
          if (path === '/dashboard') {
            const heading = document.querySelector('.dashboard-page-title');
            const textNode = Array.from(heading.childNodes).find(node => node.nodeType === Node.TEXT_NODE && node.textContent.includes('대시보드'));
            const range = document.createRange();
            range.setStart(textNode, textNode.textContent.indexOf('대시보드'));
            range.setEnd(textNode, textNode.textContent.indexOf('대시보드') + 4);
            const lines = new Set(Array.from(range.getClientRects()).map(rect => Math.round(rect.top)));
            result.dashboard = { headingWordKept: lines.size === 1, unicodeArrowVisible: bodyText.includes('→') };
          }
          if (path.startsWith('/result/') || path.startsWith('/wrong-notes/')) {
            result.review = {
              explanationPresent: Boolean(document.querySelector('.explanation-accordion .explanation-body')),
              rawSourceObjectAbsent: !bodyText.includes("{'id': 'SRC-") && !bodyText.includes('source_type'),
              aiTriggerVisible: Boolean(document.querySelector('.btn-ai-helper')),
            };
          }
          return result;
        }""",
        path,
    )
    result["status"] = response.status
    return result


def inspect_ai_modal(page):
    page.goto(BASE_URL + "/history/68", wait_until="networkidle")
    page.locator(".btn-ai-helper").first.click()
    modal_state = page.evaluate(
        """() => {
          const modal = document.getElementById('ai-prompt-modal');
          return {
            helperType: typeof window.openAIPromptModal,
            display: modal ? getComputedStyle(modal).display : null,
            inlineDisplay: modal ? modal.style.display : null,
            triggerCount: document.querySelectorAll('.btn-ai-helper').length,
            triggerHandler: document.querySelector('.btn-ai-helper')?.getAttribute('onclick'),
          };
        }"""
    )
    if modal_state["display"] == "none":
        raise RuntimeError("AI modal did not open: " + json.dumps(modal_state, ensure_ascii=False))
    initial = page.evaluate(
        """() => {
          const modal = document.querySelector('.ai-modal-card').getBoundingClientRect();
          const textarea = document.getElementById('ai-prompt-textarea');
          const links = Array.from(document.querySelectorAll('.ai-modal-actions a'));
          return {
            modalWithinViewport: modal.left >= 15 && modal.right <= window.innerWidth - 15,
            modalScrollable: getComputedStyle(document.querySelector('.ai-modal-body')).overflowY === 'auto',
            promptVisible: textarea.offsetParent !== null && textarea.value.startsWith('[ChatGPT용'),
            privacyVisible: document.querySelector('.ai-privacy-notice').offsetParent !== null,
            controlsFit: links.every(link => link.getBoundingClientRect().right <= modal.right),
            fixedProviderUrls: links.map(link => link.href),
            safeRelations: links.every(link => link.rel.includes('noopener') && link.rel.includes('noreferrer')),
          };
        }"""
    )
    page.locator('[data-provider="gemini"]').click()
    initial["geminiPromptProfile"] = page.locator("#ai-prompt-textarea").input_value().startswith("[Gemini용")
    page.locator('[data-provider="chatgpt"]').click()
    initial["chatgptPromptProfile"] = page.locator("#ai-prompt-textarea").input_value().startswith("[ChatGPT용")
    copy_result = page.evaluate(
        """async () => {
          Object.defineProperty(navigator, 'clipboard', {configurable: true, value: {writeText: () => Promise.resolve()}});
          const copied = await window.copyAIPromptText();
          return {copied, message: document.getElementById('ai-copy-status').textContent};
        }"""
    )
    failure_result = page.evaluate(
        """async () => {
          Object.defineProperty(navigator, 'clipboard', {configurable: true, value: {writeText: () => Promise.reject(new Error('blocked'))}});
          Object.defineProperty(document, 'execCommand', {configurable: true, value: () => false});
          const copied = await window.copyAIPromptText();
          const textarea = document.getElementById('ai-prompt-textarea');
          return {
            copied,
            message: document.getElementById('ai-copy-status').textContent,
            promptVisible: textarea.offsetParent !== null,
            selected: textarea.selectionStart === 0 && textarea.selectionEnd === textarea.value.length,
          };
        }"""
    )
    initial["copySuccess"] = copy_result
    initial["copyFailure"] = failure_result
    return initial


def main():
    report = {"viewports": [], "pageErrors": [], "requiredResourceFailures": [], "providerRequests": []}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True,
        )
        for width, height in VIEWPORTS:
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()
            page.on("pageerror", lambda error, w=width: report["pageErrors"].append({"width": w, "error": str(error)}))
            page.on(
                "requestfailed",
                lambda request, w=width: report["requiredResourceFailures"].append({"width": w, "url": request.url}),
            )
            page.on(
                "request",
                lambda request, w=width: report["providerRequests"].append({"width": w, "url": request.url})
                if request.url.startswith(("https://chatgpt.com", "https://gemini.google.com")) else None,
            )
            routes = [inspect_route(page, path) for path in ROUTES]
            ai = inspect_ai_modal(page)
            report["viewports"].append({"width": width, "height": height, "routes": routes, "ai": ai})
            context.close()
        browser.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
