import sys, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def convert(html_path: str, pdf_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{Path(html_path).absolute()}", wait_until="load")
        
        # Inyección táctica: elimina márgenes y fuerza continuidad
        await page.add_style_tag(content="""
            @page { margin: 0; size: auto; }
            html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; }
            * { break-inside: avoid !important; page-break-inside: avoid !important; }
        """)
        
        await page.pdf(
            path=pdf_path,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
            print_background=True
        )
        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python html2pdf_pro.py entrada.html salida.pdf")
        sys.exit(1)
    asyncio.run(convert(sys.argv[1], sys.argv[2]))
