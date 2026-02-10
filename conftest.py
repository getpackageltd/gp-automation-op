import os
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pages.base_page import BasePage
from config import OPERATOR_EMAIL, OPERATOR_PASSWORD


def pytest_addoption(parser):
    parser.addoption(
        "--test-browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use: chromium, firefox, or webkit",
    )
    parser.addoption(
        "--env",
        action="store",
        default="sandbox",
        choices=["sandbox", "stg", "dev"],
        help="Environment: sandbox, stg, or dev",
    )
    parser.addoption(
        "--view",
        action="store",
        default="false",
        choices=["true", "false"],
        help="Headed mode: true (headed) or false (headless)",
    )
    parser.addoption(
        "--lang",
        action="store",
        default="heb",
        choices=["eng", "heb"],
        help="Language for tests: eng (English) or heb (Hebrew)",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig) -> dict:
    browser_name = pytestconfig.getoption("--test-browser")
    view_mode = pytestconfig.getoption("--view")
    headless = view_mode == "false"

    launch_args = {"headless": headless}
    if browser_name == "firefox" and not headless:
        launch_args["slow_mo"] = 200
    return launch_args


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(
    pytestconfig, playwright_instance: Playwright, browser_type_launch_args: dict
) -> Generator[Browser, None, None]:
    browser_name = pytestconfig.getoption("--test-browser")
    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(**browser_type_launch_args)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(**browser_type_launch_args)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(**browser_type_launch_args)
    else:
        raise ValueError(f"Unknown browser: {browser_name}")

    env = pytestconfig.getoption("--env")
    if env == "stg":
        BasePage.url = "https://operator-stg.getpackage.dev"
        BasePage.urlOpApi = "https://api-stg.getpackage.dev"
        BasePage.authorisation = "APIKEY 8502cc15-cfee-4763-a7da-f75460f71359"
    elif env == "sandbox":
        BasePage.url = "https://frontend-sandbox.getpackage.com"
        BasePage.urlOpApi = "https://sandbox-apiv2.getpackage.com"
        BasePage.authorisation = "APIKEY 2d9ebcc2-89b5-4c36-ae4f-5835f80ef127"
    else:
        BasePage.url = os.getenv("OP_BASE_URL", "https://operator-dev.getpackage.dev")
        BasePage.urlOpApi = os.getenv("OP_API_URL", "https://api-dev.getpackage.dev")
        BasePage.authorisation = os.getenv("OP_API_KEY", "")

    yield browser
    browser.close()


@pytest.fixture(scope="session")
def storage_state_path(browser: Browser) -> Path:
    auth_dir = Path(".auth")
    auth_dir.mkdir(parents=True, exist_ok=True)
    state_path = auth_dir / "storage.json"
    if state_path.exists():
        return state_path

    context = browser.new_context()
    page = context.new_page()
    page.goto(BasePage.url + "/login")
    page.fill("//input[@placeholder='Enter your email']", OPERATOR_EMAIL)
    page.fill("//input[@placeholder='Enter your Password']", OPERATOR_PASSWORD)
    page.click("//button[contains(@class,'gp-login-btn')]//span[normalize-space()='Login']/..")
    page.wait_for_url(BasePage.url + "/deliveries")
    context.storage_state(path=str(state_path))
    context.close()
    return state_path


@pytest.fixture(scope="function")
def context(browser: Browser, request, storage_state_path: Path) -> Generator[BrowserContext, None, None]:
    try:
        import tkinter

        root = tkinter.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
    except Exception:
        width = 1920
        height = 1080

    context = browser.new_context(
        viewport={"width": width, "height": height},
        screen={"width": width, "height": height},
        accept_downloads=True,
        storage_state=str(storage_state_path),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=False)
    yield context

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        logs_dir = Path("traces")
        logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%m%d_%H%M_")
        trace_path = logs_dir / f"{timestamp}{request.node.name}.zip"
        context.tracing.stop(path=str(trace_path))
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def language(pytestconfig) -> str:
    return pytestconfig.getoption("--lang")
