let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0, 1, 2, 3, 5, 6, 7, 8]},
        {orderable: true, targets: [1, 2]},
        {searchable: false, targets: [0]}
    ],
    pageLength: 10,
    destroy: true
};
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listExpedientes();

    daTable = $('#datable-expedientes').DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

//Código para redirección de botones. Se agregó al código base. Sirve para que los botones puedan redirigir. Además, se debe configurar el código del
// botón para que la redirección surta efecto.//
const redirectToEditView = (expedienteId) => {
    // Cambia la URL de redirección según tu estructura de rutas
    window.location.href = `http://localhost:8000/Exp/edit/${expedienteId}/`;
};
//fin //

const listExpedientes = async () => {
    try {
        const response = await fetch('http://localhost:8000/Exp/list_expedientes/');
        const data = await response.json();

        let content = ``;
        data.expedientes.forEach((expedientes, index) => {
            content += `
            <tr>
            <td> ${index + 1} </td>
            <td> ${expedientes.fecha} </td>
            <td> ${expedientes.nro_exp} </td>
            <td> ${expedientes.iniciador} </td>
            <td> ${expedientes.objeto} </td>
            <td> ${expedientes.nro_resol_rectorado} </td>
            <td> ${expedientes.nro_resol_CS} </td>
            <td> ${expedientes.observaciones} </td>
            <td>
             <button class="btn btn-sm btn-primary" onclick="redirectToEditView(${expedientes.id})">
                <i class='fa-solid fa-pencil'></i></button>
                <button class="btn btn-sm btn-danger ">
                <i class='fa-solid fa-trash-can'></i></button>
                <button class="btn btn-sm btn-warning ">
                <i class="fa-regular fa-eye"></i>
                </button>
             </td>
            </tr>
            `;
        });
        tableBody_expedientes.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
});