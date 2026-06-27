{% extends "admin/base_site.html" %}
{% load i18n %}

{% block content %}
<div class="abito-dashboard">
  <section class="abito-dashboard__hero">
    <div>
      <p class="abito-eyebrow">Panel simple y rapido</p>
      <h1>Admin pensado para cargar catalogo y ordenar visitas sin vueltas</h1>
      <p class="abito-dashboard__lead">
        Usa los accesos directos para cargar prendas, actualizar precios o abrir la agenda mensual de visitas.
      </p>
    </div>
    <div class="abito-dashboard__hero-actions">
      <a href="{% url 'admin:visitas_visita_changelist' %}" class="button abito-button-primary">Abrir agenda</a>
      <a href="{% url 'admin:catalogo_traje_add' %}" class="button">Cargar traje</a>
      <a href="{% url 'admin:catalogo_combo_add' %}" class="button">Cargar combo</a>
    </div>
  </section>

  <section class="abito-shortcut-grid">
    <article class="abito-shortcut-card">
      <p class="abito-eyebrow">Visitas</p>
      <h2>Agenda mensual</h2>
      <p>Calendario por dia y horario, detalle rapido por visita y acceso a edicion manual.</p>
      <div class="abito-shortcut-card__actions">
        <a href="{% url 'admin:visitas_visita_changelist' %}" class="button abito-button-primary">Ver calendario</a>
        <a href="{% url 'admin:visitas_visita_add' %}" class="button">Nueva visita</a>
        <a href="{% url 'admin:visitas_bloqueoagenda_changelist' %}" class="button">Bloquear agenda</a>
      </div>
    </article>

    <article class="abito-shortcut-card">
      <p class="abito-eyebrow">Catalogo</p>
      <h2>Carga rapida de prendas</h2>
      <p>Subi fotos, precios y variantes sin tener que buscar cada modelo desde cero.</p>
      <div class="abito-shortcut-card__actions">
        <a href="{% url 'admin:catalogo_traje_add' %}" class="button abito-button-primary">Nuevo traje</a>
        <a href="{% url 'admin:catalogo_camisa_add' %}" class="button">Nueva camisa</a>
        <a href="{% url 'admin:catalogo_zapato_add' %}" class="button">Nuevo zapato</a>
      </div>
    </article>

    <article class="abito-shortcut-card">
      <p class="abito-eyebrow">Combos y extras</p>
      <h2>Actualizacion de precios</h2>
      <p>Entra directo a combos y accesorios para mantener todo ordenado y facil de editar.</p>
      <div class="abito-shortcut-card__actions">
        <a href="{% url 'admin:catalogo_combo_add' %}" class="button abito-button-primary">Nuevo combo</a>
        <a href="{% url 'admin:catalogo_corbata_changelist' %}" class="button">Corbatas</a>
        <a href="{% url 'admin:catalogo_cinturon_changelist' %}" class="button">Cinturones</a>
      </div>
    </article>

    <article class="abito-shortcut-card">
      <p class="abito-eyebrow">Configuracion</p>
      <h2>Mensajes y datos del sitio</h2>
      <p>Edita rapido la direccion post reserva, el mensaje de confirmacion y los canales visibles.</p>
      <div class="abito-shortcut-card__actions">
        <a href="{% url 'admin:catalogo_configuracionvisitas_changelist' %}" class="button abito-button-primary">Direccion visitas</a>
        <a href="{% url 'admin:core_configuracionsitio_changelist' %}" class="button">Sitio y canales</a>
      </div>
    </article>
  </section>

  <section class="abito-admin-list">
    <div class="abito-admin-list__header">
      <div>
        <p class="abito-eyebrow">Listado completo</p>
        <h2>Todo el admin</h2>
      </div>
      <p>Accede a cada seccion desde un panel mas ordenado, claro y consistente con el resto del admin.</p>
    </div>
    {% include "admin/app_list.html" with app_list=app_list show_changelinks=True %}
  </section>
</div>
{% endblock %}
