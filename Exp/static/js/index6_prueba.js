let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {width: '8px', targets: 0, className: 'no-toggle'},
        {width: '70px', targets: 1, className: 'no-toggle'},
        {width: '70px', targets: 2, className: 'no-toggle'},
        {width: '150px', targets: 3},
        {targets: 4, className: 'no-toggle'},
        {width: '100px', targets: 5},
        {width: '100px', targets: 6},
        {width: '150px', targets: 7},
        {width: '50px', targets: 8, className: 'no-toggle'},
        {targets: 4, className: 'justify-text'},
        {className: "centered-vertical-align", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8]},
        {className: "centered-text", targets: [0, 1, 2, 5, 6, 8]},
        {orderable: true, targets: [1, 2]},
        {searchable: false, targets: [0]},
        {
            targets: 2, // Columna donde está el número de expediente
            render: function (data) {
                // Formatear el número de expediente con ceros a la izquierda
                return data !== null ? data.toString().padStart(3, '0') : '';
            }
        },

        {
            targets: "_all",
            render: function (data) {
                return data === null ? '' : data;
            }
        }
    ],
    pageLength: 10,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    },
    dom: '<"top"lfB<"add-button-container">>rt<"bottom"ip>', // Agrega botón de agregar nuevo expediente
    buttons: [
        {
            extend: 'excelHtml5',
            text: '<i class="fas fa-file-excel"></i>', // Esto cambia el texto del botón por un ícono de Excel
            titleAttr: 'Exportar a Excel',
            className: 'btn-excel' // Esto añade las clases de botón de Bootstrap al botón
        },
         {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar a PDF',
                className: 'btn-pdf' // Asegúrate de que esta clase coincide con la que definiste en tu CSS
            },
        {
            extend: 'colvis', // Agrega el botón de mostrar/ocultar columnas
            className: 'btn-columnas-dt dropdown-toggle ',
            text: 'Columnas',
            columns: ':not(.no-toggle)', // Asegura que las columnas sin la clase 'no-toggle' sean seleccionables

        },
    ],
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listExpedientes();

    dataTable = $('#datable-expedientes_prueba').DataTable(dataTableOptions);

    // Esta línea que sigue es agregada y no forma parte del código original
    $('#datable-expedientes_prueba').css('width', '100%');


    dataTableIsInitialized = true;
};

const redirectToEditView = (expediente_pruebaId) => {
    window.location.href = `http://localhost:8000/Exp/edit_prueba/${expediente_pruebaId}/`;
};

const redirectToDeleteView = (expediente_pruebaId) => {
    window.location.href = `http://localhost:8000/Exp/eliminar_prueba/${expediente_pruebaId}/`;
};

const redirectToPaseView = (expediente_pruebaId) => {
    window.location.href = `http://localhost:8000/Exp/pase/${expediente_pruebaId}/`;
};
const redirectToDetalleView = (expediente_pruebaId) => {
    window.location.href = `http://localhost:8000/Exp/detalle_expediente/${expediente_pruebaId}/`;
};


const listExpedientes = async () => {
    try {
        const response = await fetch('http://localhost:8000/Exp/list_expedientes_prueba/');
        const data = await response.json();

        let expedientes = data.expedientes_prueba.map((expediente_prueba, index_prueba) => {
            // Obtener el área_creacion del último expediente si es nulo o vacío
            let area_creacion = expediente_prueba.area_creacion ? expediente_prueba.area_creacion : '';

            // Obtener el valor de ultimo_pase o asignar el valor de area_creacion si no hay pases
            let ultimo_pase = expediente_prueba.ultimo_pase && expediente_prueba.ultimo_pase.area_receptora ? expediente_prueba.ultimo_pase.area_receptora : area_creacion;

            // Obtener el año de la fecha de creación del expediente. Necesito colver a convertirla al formato aaaa-mm-dd para que funcione
            const partesFecha = expediente_prueba.fecha.split('/');
            const fechaCreacion = new Date(`${partesFecha[2]}-${partesFecha[1]}-${partesFecha[0]}`);
            let year = new Date(fechaCreacion).getFullYear();

            // Formatear el número de expediente con ceros a la izquierda y agregar sigla y año
            let nroExpConcatenado = `${expediente_prueba.nro_exp.toString().padStart(3, '0')}-${expediente_prueba.sigla}-${year}`;
            console.log(year)
            return [
                index_prueba + 1,
                expediente_prueba.fecha,
                nroExpConcatenado,
                expediente_prueba.iniciador,
                expediente_prueba.objeto,
                expediente_prueba.nro_resol_rectorado,
                expediente_prueba.nro_resol_CS,
                ultimo_pase,
                `
            <div class="button-container">
                <button class="btn btn-sm btn-primary" onclick="redirectToEditView(${expediente_prueba.id})" title="Editar Expediente">
                    <i class='fa-solid fa-pencil'></i>
                </button>
                
                <button class="btn btn-sm btn-danger" onclick="redirectToDeleteView(${expediente_prueba.id})" title="Eliminar Expediente">
                    <i class='fa-solid fa-trash-can'></i>
                </button>
                
                <button class="btn btn-sm custom-button" onclick="redirectToPaseView(${expediente_prueba.id})" title="Pasar Expediente">
                 <span style="color: #000000;"><i class="fa-solid fa-share"></i></span>
                </button>

                
                <button class="btn btn-sm btn-warning custom-button-size " onclick="redirectToDetalleView(${expediente_prueba.id})" title="Detalles Expediente">
                    <i class="fa-regular fa-eye"></i>
                </button>
                
            </div>
                `

            ];
        });

        dataTable = $('#datable-expedientes_prueba').DataTable({
            ...dataTableOptions,
            data: expedientes
        });

        dataTableIsInitialized = true;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();

    // Mover el botón "Columnas" al lado de la barra de búsqueda
    $('.btn-columnas-dt').detach().appendTo('.dataTables_filter');
    // Agregar un margen a la izquierda del botón
    $('.btn-columnas-dt').css('margin-left', '20px');

    $(document).ready(function () {
        $('.btn-columnas-dt').html('Columnas');
    });


    // Agregar el botón después de inicializar el DataTable
    $('.add-button-container').html(`
        <div class="btn-toolbar" role="toolbar">
            <div class="btn-group mr-2">
                <button class="btn btn-success" onclick="window.location.href='http://localhost:8000/Exp/agregar_prueba/'">
                    Agregar Nuevo Expediente
                </button>
            </div>
        </div>
    `);



    // Mover el botón "Show entries" al lado del botón "Agregar Nuevo Expediente.La separacion la hago desde el CSS"
    $('.dataTables_length').appendTo('.add-button-container .btn-toolbar');
});
