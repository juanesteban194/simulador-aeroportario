// Construye Informe_tecnico.docx a partir de informe/informe.json (lo genera generar_informe.py).
// Uso: node informe/construir_docx.js <informe.json> <salida.docx>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  BorderStyle, ShadingType, ImageRun, Header, Footer, PageNumber, LevelFormat, PageBreak, TabStopType,
} = require("docx");

const [, , entrada, salida] = process.argv;
const spec = JSON.parse(fs.readFileSync(entrada, "utf8"));
const base = path.dirname(path.resolve(entrada));

const FUENTE = "Calibri";
const MONO = "Consolas";
const AZUL = "1F4E79";
const GRIS = "595959";
const ANCHO = 9360; // carta con márgenes de 1": 6,5" = 9360 DXA

// ---------- texto con **negrita** y `código`
function corridas(texto, extra = {}) {
  const partes = texto.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).filter((p) => p !== "");
  return partes.map((p) => {
    if (p.startsWith("**") && p.endsWith("**")) return new TextRun({ text: p.slice(2, -2), bold: true, ...extra });
    if (p.startsWith("`") && p.endsWith("`"))
      return new TextRun({ text: p.slice(1, -1), font: MONO, size: 19, color: "7A2E0E", ...extra });
    return new TextRun({ text: p, ...extra });
  });
}

function parrafo(texto, opciones = {}) {
  return new Paragraph({ children: corridas(texto, opciones.run || {}), spacing: { after: 120, line: 276 },
    alignment: opciones.alineacion || AlignmentType.JUSTIFIED, ...(opciones.parrafo || {}) });
}

// ---------- tamaño de un PNG (para conservar la proporción)
function tamanoPng(ruta) {
  const b = fs.readFileSync(ruta);
  return { ancho: b.readUInt32BE(16), alto: b.readUInt32BE(20) };
}

const borde = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };

function tabla(b) {
  const columnas = b.encabezado.length;
  const anchos = b.anchos ? b.anchos.map((a) => Math.round((a / b.anchos.reduce((x, y) => x + y, 0)) * ANCHO))
    : Array(columnas).fill(Math.floor(ANCHO / columnas));
  anchos[anchos.length - 1] += ANCHO - anchos.reduce((x, y) => x + y, 0);
  const celda = (texto, i, cabecera, resaltada) => new TableCell({
    borders: bordes, width: { size: anchos[i], type: WidthType.DXA },
    shading: cabecera ? { fill: "DCE6F2", type: ShadingType.CLEAR, color: "auto" }
      : resaltada ? { fill: "FFF4D6", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      alignment: i > 0 && b.numerica ? AlignmentType.RIGHT : AlignmentType.LEFT,
      children: corridas(String(texto), { size: 19, bold: cabecera || undefined }),
    })],
  });
  return new Table({
    width: { size: ANCHO, type: WidthType.DXA }, columnWidths: anchos,
    rows: [
      new TableRow({ tableHeader: true, children: b.encabezado.map((t, i) => celda(t, i, true, false)) }),
      ...b.filas.map((fila, r) => new TableRow({
        children: fila.map((t, i) => celda(t, i, false, b.resaltar === r)),
      })),
    ],
  });
}

function bloque(b) {
  switch (b.tipo) {
    case "h1": return [new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(b.texto)] })];
    case "h2": return [new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(b.texto)] })];
    case "h3": return [new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(b.texto)] })];
    case "p": return [parrafo(b.texto)];
    case "vinetas": return b.items.map((t) => new Paragraph({ numbering: { reference: "vinetas", level: 0 },
      children: corridas(t), spacing: { after: 60, line: 264 } }));
    case "numerada": return b.items.map((t) => new Paragraph({ numbering: { reference: b.ref || "numeros", level: 0 },
      children: corridas(t), spacing: { after: 60, line: 264 } }));
    case "tabla": {
      const salida = [tabla(b)];
      if (b.pie) salida.push(new Paragraph({ children: corridas(b.pie, { italics: true, size: 18, color: GRIS }),
        spacing: { before: 60, after: 200 } }));
      else salida.push(new Paragraph({ children: [], spacing: { after: 120 } }));
      return salida;
    }
    case "imagen": {
      const ruta = path.resolve(base, b.ruta);
      const { ancho, alto } = tamanoPng(ruta);
      const anchoPx = Math.round((b.ancho_pulgadas || 6.5) * 96);
      return [
        new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
          children: [new ImageRun({ type: "png", data: fs.readFileSync(ruta),
            transformation: { width: anchoPx, height: Math.round((anchoPx * alto) / ancho) },
            altText: { title: b.pie || "Gráfico", description: b.pie || "Gráfico", name: path.basename(ruta) } })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 220 },
          children: corridas(b.pie || "", { italics: true, size: 18, color: GRIS }) }),
      ];
    }
    case "codigo": {
      const lineas = b.texto.split("\n");
      const salida = [new Paragraph({ keepNext: true, spacing: { before: 80, after: 0 },
        children: [new TextRun({ text: b.lenguaje, bold: true, size: 17, color: GRIS })] })];
      lineas.forEach((l, i) => salida.push(new Paragraph({
        keepNext: i < lineas.length - 1, spacing: { after: 0, line: 240 },
        shading: { fill: "F3F3F1", type: ShadingType.CLEAR, color: "auto" },
        children: [new TextRun({ text: l.length ? l : " ", font: MONO, size: 17 })] })));
      salida.push(new Paragraph({ children: [], spacing: { after: 100 } }));
      return salida;
    }
    case "nota": return [new Paragraph({
      children: corridas(b.texto), spacing: { before: 80, after: 160, line: 264 },
      shading: { fill: "EAF1FB", type: ShadingType.CLEAR, color: "auto" },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: "2A78D6", space: 8 } },
      indent: { left: 160, right: 160 } })];
    case "salto": return [new Paragraph({ children: [new PageBreak()] })];
    case "portada": return portada(b);
    default: throw new Error("tipo de bloque desconocido: " + b.tipo);
  }
}

function portada(b) {
  const linea = (texto, opciones) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: opciones.spacing,
    children: [new TextRun({ text: texto, font: FUENTE, ...opciones.run })] });
  return [
    linea(b.institucion, { spacing: { before: 1200, after: 120 }, run: { size: 26, color: GRIS } }),
    linea(b.curso, { spacing: { after: 1200 }, run: { size: 24, color: GRIS } }),
    linea(b.titulo, { spacing: { after: 240 }, run: { size: 48, bold: true, color: AZUL } }),
    linea(b.subtitulo, { spacing: { after: 1400 }, run: { size: 28, color: "2A78D6" } }),
    ...b.autores.map((a) => linea(a, { spacing: { after: 60 }, run: { size: 24 } })),
    linea(b.profesor, { spacing: { before: 400, after: 60 }, run: { size: 22, color: GRIS } }),
    linea(b.fecha, { spacing: { after: 60 }, run: { size: 22, color: GRIS } }),
    linea(b.repositorio, { spacing: { before: 600 }, run: { size: 20, color: "2A78D6" } }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

const doc = new Document({
  creator: spec.autor, title: spec.titulo, description: spec.descripcion,
  styles: {
    default: { document: { run: { font: FUENTE, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FUENTE, color: AZUL },
        paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FUENTE, color: AZUL },
        paragraph: { spacing: { before: 260, after: 120 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: FUENTE, color: "2A78D6" },
        paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      ...["numeros", "numeros2", "numeros3", "numeros4", "numeros5"].map((ref) => ({ reference: ref,
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] })),
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1440, right: 1440, bottom: 1300, left: 1440 } }, titlePage: true },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: spec.encabezado, size: 17, color: GRIS })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: ANCHO }],
      children: [new TextRun({ text: spec.pie, size: 17, color: GRIS }),
        new TextRun({ children: ["\tPágina ", PageNumber.CURRENT, " de ", PageNumber.TOTAL_PAGES], size: 17, color: GRIS })],
    })] }) },
    children: spec.bloques.flatMap(bloque),
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(salida, buffer);
  console.log("Informe escrito en " + salida);
});
