document.addEventListener("DOMContentLoaded", function () {
    // Inicializar DataTables si existe la tabla de equipos
    if (document.querySelector("#tabla-equipos")) {
        new DataTable("#tabla-equipos", {
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json"
            },
            responsive: true
        });
    }

    // Confirmación de eliminación
    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", function (e) {
            if (!confirm("¿Seguro que deseas eliminar este equipo?")) {
                e.preventDefault();
            }
        });
    });
});

