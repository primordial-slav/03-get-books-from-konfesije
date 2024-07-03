import os
from PIL import Image
from ebooklib import epub

def create_pdf(images, output_path):
    images[0].save(output_path, save_all=True, append_images=images[1:])
    print(f"PDF created successfully: {output_path}")

def create_epub(image_files, image_folder, output_path):
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Your Book Title')
    book.set_language('en')
    book.add_author('Author Name')

    for img_filename in image_files:
        img_path = os.path.join(image_folder, img_filename)
        epub_img = epub.EpubItem(file_name=os.path.basename(img_path), media_type='image/jpeg', content=open(img_path, 'rb').read())
        book.add_item(epub_img)

        spine_item = epub.EpubHtml(title=img_filename, file_name=f'{img_filename}.xhtml', lang='en')
        spine_item.content = f'<html><body><img src="{img_filename}" alt="{img_filename}" style="width: 100%; height: auto;"/></body></html>'
        book.add_item(spine_item)
        book.spine.append(spine_item)

    nav_css = epub.EpubItem(uid="style_nav", file_name="style/style.css", media_type="text/css", content='BODY { color: white; background-color: black; }')
    book.add_item(nav_css)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(output_path, book, {})
    print(f"EPUB created successfully: {output_path}")

def main():
    image_folder = 'temp'  # Working directory for images
    image_files = sorted([img for img in os.listdir(image_folder) if img.endswith('.jpg')], key=lambda x: int(x.split('_')[1].split('.')[0]))

    images = [Image.open(os.path.join(image_folder, img)).convert('RGB') for img in image_files]
    pdf_path = os.path.join(image_folder, 'output.pdf')
    create_pdf(images, pdf_path)

    epub_path = os.path.join(image_folder, 'output.epub')
    create_epub(image_files, image_folder, epub_path)

if __name__ == "__main__":
    main()


