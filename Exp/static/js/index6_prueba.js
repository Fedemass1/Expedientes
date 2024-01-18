
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0, 1, 2, 3, 5, 6, 7, 8]},
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
    dom: '<"top"lfB<"add-button-container">>rt<"bottom"ip>', // Agrega botón de agregar nuevo expediente
    buttons: [],
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

            return [
                index_prueba + 1,
                expediente_prueba.fecha,
                expediente_prueba.nro_exp,
                expediente_prueba.iniciador,
                expediente_prueba.objeto,
                expediente_prueba.nro_resol_rectorado,
                expediente_prueba.nro_resol_CS,
                ultimo_pase,
                `
                <button class="btn btn-sm btn-primary" onclick="redirectToEditView(${expediente_prueba.id})" title="Editar Expediente">
                    <i class='fa-solid fa-pencil'></i>
                </button>
                
                <button class="btn btn-sm btn-danger" onclick="redirectToDeleteView(${expediente_prueba.id})" title="Eliminar Expediente">
                    <i class='fa-solid fa-trash-can'></i>
                </button>
                
                <button class="btn btn-sm custom-button" onclick="redirectToPaseView(${expediente_prueba.id})" title="Pasar Expediente">
                 <span style="color: #000000;"><i class="fa-solid fa-share"></i></span>
                </button>

                
                <button class="btn btn-sm btn-warning" onclick="redirectToDetalleView(${expediente_prueba.id})" title="Detalles Expediente">
                    <i class="fa-regular fa-eye"></i>
                </button>
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
