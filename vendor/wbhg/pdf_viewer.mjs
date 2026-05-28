const paramsString = window.location.search;
const searchParams = new URLSearchParams(paramsString);
const viewerDebug = searchParams.get("pdfviewer");

if (!viewerDebug) return;


if (!pdfjsLib.getDocument || !pdfjsViewer.PDFPageView) {
  // eslint-disable-next-line no-alert
  console.log("Please build the pdfjs-dist library using\n  `gulp dist-install`");
}

// The workerSrc property shall be specified.
//
pdfjsLib.GlobalWorkerOptions.workerSrc =
  "../vendor/pdf-js/pdf.worker.mjs";

// Some PDFs need external cmaps.
//
const CMAP_URL = "../../vendor/pdf-js/cmaps/";
const CMAP_PACKED = true;

const DEFAULT_URL = "../../assets/monthly/v1i1/WBHG_Monthly_V1S1-10x12in.pdf";
const PAGE_TO_VIEW = 1;
const SCALE = 1.0;

const ENABLE_XFA = true;

const container = document.getElementById("pdf-canvas-wrapper");
const toolbar = document.getElementById("pdfToolbar");

async function initPdfJS() {

  const eventBus = new pdfjsViewer.EventBus();

  // Loading document.
  const loadingTask = pdfjsLib.getDocument({
    url: DEFAULT_URL,
    cMapUrl: CMAP_URL,
    cMapPacked: CMAP_PACKED,
    enableXfa: ENABLE_XFA,
  });

  const pdfDocument = await loadingTask.promise;
  // Document loaded, retrieving the page.
  const pdfPage = await pdfDocument.getPage(PAGE_TO_VIEW);

  // Creating the page view with default parameters.
  const pdfPageView = new pdfjsViewer.PDFPageView({
    container,
    id: PAGE_TO_VIEW,
    scale: SCALE,
    defaultViewport: pdfPage.getViewport({ scale: SCALE }),
    eventBus,
  });
  // Associate the actual page with the view, and draw it.
  pdfPageView.setPdfPage(pdfPage);
  pdfPageView.draw();

}

if (viewerDebug === 'true' && container && toolbar) {
  container.classList.toggle("hidden");
  toolbar.classList.toggle("hidden");
  initPdfJS();
}