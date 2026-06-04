{% extends "admin/base_site.html" %}
{% load i18n %}

{% block breadcrumbs %}
<div class="breadcrumbs">
  <a href="{% url 'admin:index' %}">Inicio</a>
  &rsaquo;
  <a href="{% url 'admin:app_list' app_label='visitas' %}">Visitas</a>
  &rsaquo;
  Agenda
</div>
{% endblock %}

{% block content %}
{{ day_payloads|json_script:"agendaDayPayloads" }}
{{ selected_day_key|json_script:"agendaSelectedDayKey" }}
{{ selected_visit_id|json_script:"agendaSelectedVisitId" }}

<div class="abito-agenda">
  <section class="abito-agenda__hero">
    <div>
      <p class="abito-eyebrow">Visitas ordenadas por dia y horario</p>
      <h1>Elegi un dia con visitas y entra al detalle completo de cada reserva</h1>
      <p class="abito-agenda__lead">
        Primero toca el dia en el calendario. Despues, en la columna de horarios, toca la visita para ver toda su ficha: nombre, celular, cantidad, evento, catalogo visto y observaciones.
      </p>
    </div>
    <div class="abito-agenda__hero-actions">
      <a href="{% url 'admin:visitas_visita_add' %}" class="button abito-button-primary">Nueva visita</a>
      <a href="{% url 'admin:visitas_bloqueoagenda_add' %}" class="button">Bloquear horario</a>
      <a href="{{ list_url }}" class="button">Ver listado</a>
    </div>
  </section>

  <section class="abito-stats-grid">
    <article class="abito-stat-card">
      <span class="abito-stat-card__label">Visitas del mes</span>
      <strong>{{ month_visit_count }}</strong>
    </article>
    <article class="abito-stat-card">
      <span class="abito-stat-card__label">Personas agendadas</span>
      <strong>{{ month_people_count }}</strong>
    </article>
    <article class="abito-stat-card">
      <span class="abito-stat-card__label">Dias con actividad</span>
      <strong>{{ active_day_count }}</strong>
    </article>
  </section>

  <section class="abito-agenda__calendar-panel">
    <div class="abito-agenda__toolbar">
      <a href="?mes={{ previous_month }}" class="button">Mes anterior</a>

      <form method="get" class="abito-agenda__month-form">
        <div>
          <p class="abito-eyebrow">Calendario mensual</p>
          <h2>{{ month_label|capfirst }}</h2>
        </div>
        <div class="abito-agenda__month-controls">
          <label for="agenda-month-picker">Ir a mes</label>
          <input
            type="month"
            id="agenda-month-picker"
            name="mes"
            value="{{ month_value }}"
            onchange="this.form.submit()"
          >
          <input type="hidden" id="agendaSelectedDate" name="fecha" value="{{ selected_day_key }}">
          <input type="hidden" id="agendaSelectedVisit" name="visita" value="{{ selected_visit_id }}">
        </div>
      </form>

      <a href="?mes={{ next_month }}" class="button">Mes siguiente</a>
    </div>

    <p class="abito-agenda__hint">
      Los dias con visitas aparecen como botones marcados. En celular podes deslizar el calendario si hace falta.
    </p>

    <div class="abito-calendar-shell">
      <div class="abito-calendar-weekdays">
        <span>Lun</span>
        <span>Mar</span>
        <span>Mie</span>
        <span>Jue</span>
        <span>Vie</span>
        <span>Sab</span>
        <span>Dom</span>
      </div>

      <div class="abito-calendar-grid">
        {% for week in calendar_rows %}
          {% for cell in week %}
            {% if cell.is_current_month and cell.has_activity %}
              <button
                type="button"
                class="abito-day-card has-activity{% if cell.is_selected %} is-selected{% endif %}{% if cell.is_today %} is-today{% endif %}"
                data-agenda-day
                data-date="{{ cell.date_key }}"
                data-label="{{ cell.date|date:'l j \\d\\e F \\d\\e Y' }}"
                data-count="{{ cell.visit_count }}"
                aria-pressed="{% if cell.is_selected %}true{% else %}false{% endif %}"
              >
                <span class="abito-day-card__top">
                  <span class="abito-day-card__number">{{ cell.day_number }}</span>
                  {% if cell.is_today %}
                    <span class="abito-day-card__tag">Hoy</span>
                  {% endif %}
                </span>
                <span class="abito-day-card__summary">{{ cell.visit_count }} visitas</span>
                <span class="abito-day-card__summary abito-day-card__summary--soft">
                  {{ cell.people_count }} personas
                </span>
                <span class="abito-slot-list">
                  {% for slot in cell.time_slots %}
                    <span class="abito-slot-chip">{{ slot.label }} | {{ slot.visit_count }}</span>
                  {% endfor %}
                  {% if cell.extra_slot_count %}
                    <span class="abito-slot-chip is-muted">+{{ cell.extra_slot_count }} horarios</span>
                  {% endif %}
                </span>
              </button>
            {% else %}
              <div class="abito-day-card{% if not cell.is_current_month %} is-outside-month{% endif %}{% if cell.is_selected %} is-selected{% endif %}" aria-hidden="{% if not cell.is_current_month %}true{% else %}false{% endif %}">
                <span class="abito-day-card__top">
                  <span class="abito-day-card__number">{{ cell.day_number }}</span>
                  {% if cell.is_today %}
                    <span class="abito-day-card__tag">Hoy</span>
                  {% endif %}
                </span>
                {% if cell.is_current_month %}
                  <span class="abito-day-card__empty">Sin visitas</span>
                {% endif %}
              </div>
            {% endif %}
          {% endfor %}
        {% endfor %}
      </div>
    </div>
  </section>

  <section class="abito-day-detail">
    <div class="abito-day-detail__header">
      <div>
        <p class="abito-eyebrow">Agenda del dia</p>
        <h2 id="agendaDayTitle">{{ selected_day_label|capfirst }}</h2>
      </div>
      <p class="abito-day-detail__count" id="agendaDayCount">
        {{ selected_day_payload.visits|length }} visita{{ selected_day_payload.visits|length|pluralize }}
      </p>
    </div>

    <div class="abito-day-layout">
      <div class="abito-day-schedule">
        <div class="abito-day-schedule__header">
          <div>
            <p class="abito-eyebrow">Horarios del dia</p>
            <h3>Selecciona una visita</h3>
          </div>
          <p class="abito-day-schedule__note">
            Cada bloque muestra las visitas cargadas en ese horario.
          </p>
        </div>

        <div id="agendaDaySlots" class="abito-day-slots">
          {% for slot in selected_day_payload.slots %}
            <article class="abito-hour-card">
              <div class="abito-hour-card__head">
                <span class="abito-time-pill">{{ slot.label }}</span>
                <span class="abito-hour-card__meta">
                  {% if slot.visit_count %}
                    {{ slot.visit_count }} visita{{ slot.visit_count|pluralize }} | {{ slot.people_count }} persona{{ slot.people_count|pluralize }}
                  {% else %}
                    Sin visitas
                  {% endif %}
                </span>
              </div>

              <div class="abito-hour-card__body">
                {% for visit in slot.visits %}
                  <button
                    type="button"
                    class="abito-visit-button{% if visit.id == selected_visit_id %} is-active{% endif %}"
                    data-agenda-visit
                    data-visit-id="{{ visit.id }}"
                  >
                    <span class="abito-visit-button__name">{{ visit.nombre }}</span>
                    <span class="abito-visit-button__meta">{{ visit.telefono }}</span>
                    <span class="abito-visit-button__meta">{{ visit.cantidad_personas }} persona{{ visit.cantidad_personas|pluralize }}</span>
                  </button>
                {% empty %}
                  <div class="abito-hour-card__empty">
                    No hay visitas en este horario.
                  </div>
                {% endfor %}
              </div>
            </article>
          {% endfor %}
        </div>
      </div>

      <div class="abito-visit-detail">
        <div id="agendaVisitEmpty" class="abito-empty-state{% if selected_visit %} is-hidden{% endif %}">
          Este dia no tiene visitas cargadas. Cuando selecciones un dia con actividad, aca vas a ver la ficha completa.
        </div>

        <div id="agendaVisitPanel"{% if not selected_visit %} class="is-hidden"{% endif %}>
          {% if selected_visit %}
            <div class="abito-visit-card">
              <div class="abito-visit-card__hero">
                <div>
                  <p class="abito-eyebrow">Detalle de la visita</p>
                  <h3>{{ selected_visit.nombre }}</h3>
                  <p class="abito-visit-card__sub">
                    {{ selected_visit.hora }} | {{ selected_visit.fecha_visita }} | {{ selected_visit.estado }}
                  </p>
                </div>
                <a href="{{ selected_visit.admin_url }}" class="button abito-button-primary">Abrir ficha completa</a>
              </div>

              <div class="abito-visit-meta-grid">
                <article class="abito-visit-meta-card">
                  <span>Celular</span>
                  <strong>{{ selected_visit.telefono }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>DNI</span>
                  <strong>{{ selected_visit.dni }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Cantidad</span>
                  <strong>{{ selected_visit.cantidad_personas }} persona{{ selected_visit.cantidad_personas|pluralize }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Fecha del evento</span>
                  <strong>{{ selected_visit.fecha_evento }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Fecha de visita</span>
                  <strong>{{ selected_visit.fecha_visita }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Horario</span>
                  <strong>{{ selected_visit.hora }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Estado</span>
                  <strong>{{ selected_visit.estado }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Origen</span>
                  <strong>{{ selected_visit.origen }}</strong>
                </article>
                <article class="abito-visit-meta-card">
                  <span>Vio catalogo</span>
                  <strong>{{ selected_visit.vio_catalogo }}</strong>
                </article>
              </div>

              <div class="abito-visit-section">
                <div class="abito-visit-section__header">
                  <h4>Ambos y talles vistos en catalogo</h4>
                  <span>{{ selected_visit.cantidad_preferencias }} cargados</span>
                </div>

                <div id="agendaVisitPreferences" class="abito-preferences-list">
                  {% for preference in selected_visit.preferencias %}
                    <article class="abito-preference-card">
                      <strong>Ambo {{ preference.orden }}</strong>
                      <p>{{ preference.linea }} - {{ preference.tela }}</p>
                      <p>Color {{ preference.color }} | Saco {{ preference.talle_saco }} | Pantalon {{ preference.talle_pantalon }}</p>
                    </article>
                  {% empty %}
                    <div class="abito-hour-card__empty">
                      No cargo ambos o talles para esta visita.
                    </div>
                  {% endfor %}
                </div>
              </div>

              <div class="abito-visit-section">
                <div class="abito-visit-section__header">
                  <h4>Observaciones internas</h4>
                </div>
                <div id="agendaVisitNotes" class="abito-note-card">
                  {{ selected_visit.observaciones }}
                </div>
              </div>

              <div class="abito-visit-foot">
                <span>Creada: {{ selected_visit.creado }}</span>
                <span>Actualizada: {{ selected_visit.actualizado }}</span>
              </div>
            </div>
          {% endif %}
        </div>
      </div>
    </div>
  </section>
</div>

<script>
  (function() {
    const payloadSource = document.getElementById("agendaDayPayloads");
    if (!payloadSource) {
      return;
    }

    const payloadMap = JSON.parse(payloadSource.textContent);
    const selectedDaySource = document.getElementById("agendaSelectedDayKey");
    const selectedVisitSource = document.getElementById("agendaSelectedVisitId");
    const selectedDateInput = document.getElementById("agendaSelectedDate");
    const selectedVisitInput = document.getElementById("agendaSelectedVisit");
    const dayButtons = Array.from(document.querySelectorAll("[data-agenda-day]"));
    const dayTitleNode = document.getElementById("agendaDayTitle");
    const dayCountNode = document.getElementById("agendaDayCount");
    const slotContainer = document.getElementById("agendaDaySlots");
    const visitEmptyNode = document.getElementById("agendaVisitEmpty");
    const visitPanelNode = document.getElementById("agendaVisitPanel");
    const currentMonth = "{{ month_value }}";
    const agendaHours = {{ "['17:00', '17:30', '18:00', '18:30', '19:00', '19:30']"|safe }};

    const state = {
      dayKey: selectedDaySource ? JSON.parse(selectedDaySource.textContent) : "",
      visitId: selectedVisitSource ? Number(JSON.parse(selectedVisitSource.textContent) || 0) || null : null
    };

    function escapeHtml(value) {
      return String(value == null ? "" : value).replace(/[&<>"']/g, function(char) {
        return {
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          "\"": "&quot;",
          "'": "&#39;"
        }[char];
      });
    }

    function pluralize(value, singular, plural) {
      return Number(value) === 1 ? singular : plural;
    }

    function buildEmptyDayPayload() {
      return {
        visits: [],
        slots: agendaHours.map(function(hour) {
          return {
            hora: hour,
            label: hour,
            visit_count: 0,
            people_count: 0,
            visits: []
          };
        })
      };
    }

    function getDayPayload(dayKey) {
      return payloadMap[dayKey] || buildEmptyDayPayload();
    }

    function getSelectedDayButton() {
      return dayButtons.find(function(button) {
        return button.dataset.date === state.dayKey;
      }) || null;
    }

    function updateUrl() {
      const url = new URL(window.location.href);
      url.searchParams.set("mes", currentMonth);

      if (state.dayKey) {
        url.searchParams.set("fecha", state.dayKey);
      } else {
        url.searchParams.delete("fecha");
      }

      if (state.visitId) {
        url.searchParams.set("visita", state.visitId);
      } else {
        url.searchParams.delete("visita");
      }

      window.history.replaceState({}, "", url);
    }

    function renderSlots(dayPayload) {
      slotContainer.innerHTML = dayPayload.slots.map(function(slot) {
        const visitButtons = slot.visits.map(function(visit) {
          return [
            '<button type="button" class="abito-visit-button',
            visit.id === state.visitId ? ' is-active' : '',
            '" data-agenda-visit data-visit-id="',
            escapeHtml(visit.id),
            '">',
            '<span class="abito-visit-button__name">',
            escapeHtml(visit.nombre),
            '</span>',
            '<span class="abito-visit-button__meta">',
            escapeHtml(visit.telefono),
            '</span>',
            '<span class="abito-visit-button__meta">',
            escapeHtml(visit.cantidad_personas),
            ' ',
            pluralize(visit.cantidad_personas, 'persona', 'personas'),
            '</span>',
            '</button>'
          ].join("");
        }).join("");

        const slotMeta = slot.visit_count
          ? escapeHtml(slot.visit_count) + " " + pluralize(slot.visit_count, "visita", "visitas") + " | " + escapeHtml(slot.people_count) + " " + pluralize(slot.people_count, "persona", "personas")
          : "Sin visitas";

        return [
          '<article class="abito-hour-card">',
          '<div class="abito-hour-card__head">',
          '<span class="abito-time-pill">',
          escapeHtml(slot.label),
          '</span>',
          '<span class="abito-hour-card__meta">',
          slotMeta,
          '</span>',
          '</div>',
          '<div class="abito-hour-card__body">',
          visitButtons || '<div class="abito-hour-card__empty">No hay visitas en este horario.</div>',
          '</div>',
          '</article>'
        ].join("");
      }).join("");

      slotContainer.querySelectorAll("[data-agenda-visit]").forEach(function(button) {
        button.addEventListener("click", function() {
          selectVisit(Number(button.dataset.visitId));
        });
      });
    }

    function renderPreferences(preferences) {
      if (!preferences.length) {
        return '<div class="abito-hour-card__empty">No cargo ambos o talles para esta visita.</div>';
      }

      return preferences.map(function(preference) {
        return [
          '<article class="abito-preference-card">',
          '<strong>Ambo ',
          escapeHtml(preference.orden),
          '</strong>',
          '<p>',
          escapeHtml(preference.linea),
          ' - ',
          escapeHtml(preference.tela),
          '</p>',
          '<p>Color ',
          escapeHtml(preference.color),
          ' | Saco ',
          escapeHtml(preference.talle_saco),
          ' | Pantalon ',
          escapeHtml(preference.talle_pantalon),
          '</p>',
          '</article>'
        ].join("");
      }).join("");
    }

    function renderVisit(visit) {
      if (!visit) {
        visitPanelNode.innerHTML = "";
        visitPanelNode.classList.add("is-hidden");
        visitEmptyNode.classList.remove("is-hidden");
        return;
      }

      visitEmptyNode.classList.add("is-hidden");
      visitPanelNode.classList.remove("is-hidden");
      visitPanelNode.innerHTML = [
        '<div class="abito-visit-card">',
        '<div class="abito-visit-card__hero">',
        '<div>',
        '<p class="abito-eyebrow">Detalle de la visita</p>',
        '<h3>',
        escapeHtml(visit.nombre),
        '</h3>',
        '<p class="abito-visit-card__sub">',
        escapeHtml(visit.hora),
        ' | ',
        escapeHtml(visit.fecha_visita),
        ' | ',
        escapeHtml(visit.estado),
        '</p>',
        '</div>',
        '<a href="',
        escapeHtml(visit.admin_url),
        '" class="button abito-button-primary">Abrir ficha completa</a>',
        '</div>',
        '<div class="abito-visit-meta-grid">',
        '<article class="abito-visit-meta-card"><span>Celular</span><strong>',
        escapeHtml(visit.telefono),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>DNI</span><strong>',
        escapeHtml(visit.dni),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Cantidad</span><strong>',
        escapeHtml(visit.cantidad_personas),
        ' ',
        pluralize(visit.cantidad_personas, 'persona', 'personas'),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Fecha del evento</span><strong>',
        escapeHtml(visit.fecha_evento),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Fecha de visita</span><strong>',
        escapeHtml(visit.fecha_visita),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Horario</span><strong>',
        escapeHtml(visit.hora),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Estado</span><strong>',
        escapeHtml(visit.estado),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Origen</span><strong>',
        escapeHtml(visit.origen),
        '</strong></article>',
        '<article class="abito-visit-meta-card"><span>Vio catalogo</span><strong>',
        escapeHtml(visit.vio_catalogo),
        '</strong></article>',
        '</div>',
        '<div class="abito-visit-section">',
        '<div class="abito-visit-section__header">',
        '<h4>Ambos y talles vistos en catalogo</h4>',
        '<span>',
        escapeHtml(visit.cantidad_preferencias),
        ' cargados</span>',
        '</div>',
        '<div class="abito-preferences-list">',
        renderPreferences(visit.preferencias || []),
        '</div>',
        '</div>',
        '<div class="abito-visit-section">',
        '<div class="abito-visit-section__header"><h4>Observaciones internas</h4></div>',
        '<div class="abito-note-card">',
        escapeHtml(visit.observaciones || "-"),
        '</div>',
        '</div>',
        '<div class="abito-visit-foot">',
        '<span>Creada: ',
        escapeHtml(visit.creado || "-"),
        '</span>',
        '<span>Actualizada: ',
        escapeHtml(visit.actualizado || "-"),
        '</span>',
        '</div>',
        '</div>'
      ].join("");
    }

    function updateDaySelectionUI() {
      dayButtons.forEach(function(button) {
        const isSelected = button.dataset.date === state.dayKey;
        button.classList.toggle("is-selected", isSelected);
        button.setAttribute("aria-pressed", isSelected ? "true" : "false");
      });
    }

    function updateDayHeader(dayPayload) {
      const selectedButton = getSelectedDayButton();
      if (selectedButton) {
        const label = selectedButton.dataset.label;
        const count = Number(selectedButton.dataset.count || dayPayload.visits.length || 0);
        dayTitleNode.textContent = label.charAt(0).toUpperCase() + label.slice(1);
        dayCountNode.textContent = count + " " + pluralize(count, "visita", "visitas");
        return;
      }

      dayTitleNode.textContent = "{{ selected_day_label|capfirst }}";
      dayCountNode.textContent = dayPayload.visits.length + " " + pluralize(dayPayload.visits.length, "visita", "visitas");
    }

    function selectVisit(visitId) {
      const dayPayload = getDayPayload(state.dayKey);
      const nextVisit = dayPayload.visits.find(function(visit) {
        return visit.id === visitId;
      }) || dayPayload.visits[0] || null;

      state.visitId = nextVisit ? nextVisit.id : null;
      selectedVisitInput.value = state.visitId || "";

      renderSlots(dayPayload);
      renderVisit(nextVisit);
      updateUrl();
    }

    function selectDay(dayKey) {
      state.dayKey = dayKey;
      selectedDateInput.value = dayKey;

      const dayPayload = getDayPayload(dayKey);
      const nextVisit = dayPayload.visits.find(function(visit) {
        return visit.id === state.visitId;
      }) || dayPayload.visits[0] || null;

      state.visitId = nextVisit ? nextVisit.id : null;
      selectedVisitInput.value = state.visitId || "";

      updateDaySelectionUI();
      updateDayHeader(dayPayload);
      renderSlots(dayPayload);
      renderVisit(nextVisit);
      updateUrl();
    }

    dayButtons.forEach(function(button) {
      button.addEventListener("click", function() {
        selectDay(button.dataset.date);
      });
    });

    renderSlots(getDayPayload(state.dayKey));
    renderVisit(
      getDayPayload(state.dayKey).visits.find(function(visit) {
        return visit.id === state.visitId;
      }) || getDayPayload(state.dayKey).visits[0] || null
    );
  })();
</script>
{% endblock %}
