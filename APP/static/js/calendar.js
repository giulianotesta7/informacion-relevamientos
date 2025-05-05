document.addEventListener('DOMContentLoaded', function() {
    let request_calendar = "./static/data/events.json";

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        events: function(info, successCallback, failureCallback){
            fetch(request_calendar)
                .then(response => response.json())
                .then(data => {
                    let events = data.events.map(event => {
                        return {
                            title: event.eventTitle,
                            start: new Date(event.eventStartDate),
                            end: new Date(event.eventEndDate),
                            url: event.eventUrl,
                            extendedProps: {
                                location: event.eventLocation,
                                timeStart: event.eventStartTime,
                                timeEnd: event.eventEndTime,
                                technician: event.eventTechnician
                            }
                        }
                    });
                    successCallback(events);
                })
                .catch(error => failureCallback(error));
        },

        eventContent: function(info){
            return {
                html: `
                <div style="overflow: hidden; font-size: 12px; position: relative; cursor: pointer; font-family: 'Inter', sans-serif;">
                    <div><strong>${info.event.title}</strong></div>
                    <div>Ubicación: ${info.event.extendedProps.location}</div>
                    <div>Técnico: ${info.event.extendedProps.technician}</div>
                </div>
                `
            }
        },

        eventMouseEnter: function(mouseEnterInfo){
            let el = mouseEnterInfo.el;
            el.classList.add("relative");

            let tooltip = document.createElement("div");
            tooltip.innerHTML = `
                <div class="fc-hoverable-event"
                    style="position: absolute; bottom: 100%; left: 0; width: 300px; background-color: white; z-index: 50; border: 1px solid #e2e8f0; border-radius: 0.375rem; padding: 0.75rem; font-size: 14px; font-family: 'Inter', sans-serif; cursor: pointer;">
                    <strong>${mouseEnterInfo.event.title}</strong>
                    <div>Ubicación: ${mouseEnterInfo.event.extendedProps.location}</div>
                    <div>Técnico: ${mouseEnterInfo.event.extendedProps.technician}</div>
                </div>
            `;
            el.after(tooltip);
        },

        eventMouseLeave: function(){
            let tooltip = document.querySelector(".fc-hoverable-event");
            if (tooltip) tooltip.remove();
        }
    });

    calendar.render();
});
