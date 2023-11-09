import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';

(async () => {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([600, 400]);
  const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);

  const contentStream = pdfDoc.register(
    page.drawText('Пример PDF-документа', {
      x: 50,
      y: 300,
      size: 30,
      font: helveticaFont, // Используем шрифт Helvetica
      color: rgb(0, 0, 0),
    })
  );

  page.pushOperators(contentStream);

  const jsCode = `
    var title = this.info.Title;
    if (title === "") {
        title = "Документ без заголовка";
    }
    title = title + " (изменен JavaScript)";
    this.info.Title = title;
  `;

  page.pushOperators(`/${pdfDoc.register(jsCode)} exec`);

  const password = 'myPassword'; // Задайте пароль
  pdfDoc.setEncryption({
    userPassword: password,
    ownerPassword: password,
    permissions: ['print', 'copy'],
  });

  const pdfBytes = await pdfDoc.save();

  fs.writeFileSync('protected_example.pdf', pdfBytes);
})();
