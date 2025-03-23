import { useEffect, useState } from 'react'
import { NavLink, useParams } from 'react-router-dom'
import { Document, Page } from 'react-pdf';

import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import './BookDetail.css'

const BookDetail = () => {
  const { id } = useParams()
  const [book, setBook] = useState()
  const [loading, setLoading] = useState(false)
  const [pdfUrl, setPdfUrl] = useState('')
  const [numPages, setNumPages] = useState()
  const [pdfLoading, setPdfLoading] = useState(false)

  // Cargar datos del libro
  useEffect(() => {
    const fetchBook = async () => {
      setLoading(true)
      try {
        const response = await axios.get(`http://localhost:8000/api/libros/${id}`)
        setBook(response.data)
      } catch (error) {
        console.error('Error cargando libro:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchBook()
  }, [id])

  // Cargar PDF cuando el usuario haga clic
  const cargarPDF = async () => {
    if (!book) return

    setPdfLoading(true)
    try {
      const response = await axios.get(`http://localhost:8000/api/libro/${id}/url`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      setPdfUrl(response.data.url)
    } catch (error) {
      console.error('Error cargando PDF:', error)
    } finally {
      setPdfLoading(false)
    }
  }

  if (loading)
    return (
      <div className='flex gap-2 text-2xl justify-center mt-20'>
        <Loader2 className='animate-spin' /> Cargando libro...
      </div>
    )

  if (!book) return <BookNotFound />

  return (
    <section className='max-w-6xl mx-auto pb-10 px-4'>
      <div className='flex items-center gap-4 mb-6'>
        <NavLink
          to='/explore'
          className='rounded-full bg-muted p-3 hover:bg-slate-200 transition-colors'
        >
          <ArrowLeft />
        </NavLink>
        <h1 className='text-2xl font-semibold'>Información del libro</h1>
      </div>


        {/* Sección derecha - Visor PDF */}
        <div className='sticky top-4 h-fit'>
          <div className='bg-white p-4 rounded-xl shadow-lg border'>
            {pdfUrl ? (
              <div className='relative'>
                <Document
                  file={pdfUrl}
                  onLoadSuccess={({ numPages }) => setNumPages(numPages)}
                  loading={
                    <div className='flex justify-center p-8'>
                      <Loader2 className='animate-spin' />
                    </div>
                  }
                >
                  <Page
                    pageNumber={1}
                    renderAnnotationLayer={false}
                    renderTextLayer={false}
                    width={500}
                  />

                  {numPages && numPages > 1 && (
                    <div className='mt-4 text-center text-sm text-gray-500'>
                      Desplázate para ver más páginas
                    </div>
                  )}
                </Document>
              </div>
            ) : (
              <div className='flex flex-col items-center justify-center min-h-[300px] space-y-4'>
                {pdfLoading ? (
                  <>
                    <Loader2 className='animate-spin w-8 h-8' />
                    <p className='text-gray-500'>Cargando libro...</p>
                  </>
                ) : (
                  <>
                    <p className='text-gray-600 text-center mb-4'>
                      Para ver el contenido del libro, haz clic en el botón inferior
                    </p>
                    <button
                      onClick={cargarPDF}
                      className='bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors'
                    >
                      Ver libro
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
    </section>
  )
}

export default BookDetail