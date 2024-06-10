document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: agendamentos.map(function(agendamento) {
            return {
                title: `${agendamento.tipo} - ${agendamento.utente_nome}`,
                start: `${agendamento.data}T${agendamento.hora}`,
                url: agendamento.url
            };
        }),
        eventClick: function(info) {
            info.jsEvent.preventDefault(); // don't let the browser navigate

            if (info.event.url) {
                window.open(info.event.url);
            }
        }
    });

    calendar.render();
});
