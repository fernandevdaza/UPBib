import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Document, Page, pdfjs } from 'react-pdf';
import { FaSpinner } from 'react-icons/fa';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import './LectorPDF.css';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

const LectorPDF = () => {
  const { id } = useParams();
  const [pdfUrl, setPdfUrl] = useState('');
  const [numPages, setNumPages] = useState(0);
  const [virtualPages, setVirtualPages] = useState(1);
  const [pageNumber, setPageNumber] = useState(1);
  const [currentPdfPages, setCurrentPdfPages] = useState(0);
  const [pdfLoading, setPdfLoading] = useState(false);

const blobToURL = (blob) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
      const base64data = reader.result;
      resolve(base64data);
    };
  });
};

const cargarPDF = async () => {
  setPdfLoading(true);
  try {
    const response = await fetch(`http://localhost:8000/librero/api/lector/${id}?pagina=${pageNumber}`, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
      },
    });
    console.log(response.headers)
    if (!response.ok) throw new Error('Error cargando PDF');
    const totalPages = response.headers.get('X-Total-Pages');
    const totalVirtualPages = response.headers.get('X-Total-Virtual-Pages');

    // Asegúrate de revocar el objeto URL anterior si existe
    if (pdfUrl) {
      URL.revokeObjectURL(pdfUrl); // Revoca la URL anterior
    }

    const blob = await response.blob();
    const url = await blobToURL(blob);

    setPdfUrl(url);

    if (totalPages) setNumPages(parseInt(totalPages));
    if (totalVirtualPages) setVirtualPages(parseInt(totalVirtualPages));

  } catch (error) {
    console.error('Error:', error);
    alert(error.message);
  } finally {
    setPdfLoading(false);
  }
};
  useEffect(() => {
    if (id && pageNumber > 0 && pageNumber <= virtualPages) {
      cargarPDF();
    }
  }, [id, pageNumber, virtualPages]);


  useEffect(() => {
    return () => {
      if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    };
  }, [pdfUrl]);

  const goToPrevPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  const goToNextPage = () => {
    if (pageNumber < virtualPages) {
      setPageNumber(pageNumber + 1);
    }
  };

  const onLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  if (pdfLoading) {
    return (
      <div className="flex justify-center items-center h-full">
        <FaSpinner className="animate-spin text-xl" /> Cargando PDF...
      </div>
    );
  }

  return (
    <section className="max-w-6xl mx-auto pb-10 px-4">
      <div className="pdf-container">
        {pdfUrl && (
            <Document
              file={pdfUrl}
              onLoadSuccess={({ numPages }) => setCurrentPdfPages(numPages)}
              loading={<div className="flex justify-center p-8"><FaSpinner className="animate-spin" /></div>}
            >
              <div className="pages-wrapper">
                <div className="page-container">
                  <Page pageNumber={2 * pageNumber - 1} />
                </div>
                {currentPdfPages >= 2 && (
                  <div className="page-container">
                    <Page pageNumber={2 * pageNumber} />
                  </div>
                )}
              </div>
            </Document>
        )}
        <div className="pagination">
          <button
              onClick={goToPrevPage}
              disabled={pageNumber === 1}
              className="pagination-button"
          >
            Anterior
          </button>
          <span>
    Página {pageNumber} de {virtualPages || 1}
  </span>
          <button
              onClick={goToNextPage}
              disabled={pageNumber >= virtualPages || virtualPages === 0}
              className="pagination-button"
          >
            Siguiente
          </button>
        </div>
      </div>
    </section>
  );
};

export default LectorPDF;
