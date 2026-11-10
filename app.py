"""Streamlit interface for software requests and architecture review decisions."""
import streamlit as st
from database import (STATUSES, initialize_database, add_request, get_requests,
                      add_review, get_review_history)

st.set_page_config(page_title='Software Request Review', page_icon='🗂️', layout='wide')
initialize_database()
st.title('Software Request Review System')
st.caption('Fictional portfolio demonstration. Not a production approval or security assessment system.')

requests = get_requests()
a, b, c, d = st.columns(4)
a.metric('Total requests', len(requests))
b.metric('Pending', sum(r['status'] == 'Pending' for r in requests))
c.metric('In review', sum(r['status'] == 'In Review' for r in requests))
d.metric('Approved', sum(r['status'] == 'Approved' for r in requests))

submit_tab, browse_tab, review_tab = st.tabs(['Submit request', 'Browse requests', 'Architecture review'])
with submit_tab:
    st.subheader('New software request')
    with st.form('request_form', clear_on_submit=True):
        software_name = st.text_input('Software name *')
        department = st.text_input('Requesting department *')
        justification = st.text_area('Business justification *')
        estimated_cost = st.number_input('Estimated cost (USD)', min_value=0.0,
                                         step=100.0, format='%.2f')
        security_notes = st.text_area('Security considerations')
        integration_notes = st.text_area('Integration requirements')
        submitted = st.form_submit_button('Submit request')
    if submitted:
        try:
            request_id = add_request(software_name, department, justification,
                                     estimated_cost, security_notes, integration_notes)
        except (ValueError, TypeError) as error:
            st.error(str(error))
        else:
            st.success(f'Request #{request_id} saved.')
            st.rerun()

with browse_tab:
    st.subheader('Saved requests')
    status_filter = st.selectbox('Filter by status', ['All', *STATUSES])
    visible = [r for r in requests if status_filter == 'All' or r['status'] == status_filter]
    if visible:
        st.dataframe(visible, use_container_width=True, hide_index=True)
    else:
        st.info('No requests match this filter.')

with review_tab:
    st.subheader('Architecture review and decision history')
    if not requests:
        st.info('Submit a request before reviewing it.')
    else:
        request_by_id = {r['id']: r for r in requests}
        selected_id = st.selectbox('Select request', list(request_by_id),
                                   format_func=lambda rid: f"#{rid} — {request_by_id[rid]['software_name']}")
        selected = request_by_id[selected_id]
        st.write('**Current status:**', selected['status'])
        st.write('**Business justification:**', selected['justification'])
        st.write('**Original security considerations:**', selected['security_notes'] or 'Not specified')
        st.write('**Original integration requirements:**', selected['integration_notes'] or 'Not specified')
        with st.form('review_form', clear_on_submit=True):
            reviewer = st.text_input('Reviewer name *')
            new_status = st.selectbox('Decision status', STATUSES,
                                      index=STATUSES.index(selected['status']))
            security_findings = st.text_area('Security findings')
            integration_findings = st.text_area('Integration findings')
            decision_notes = st.text_area('Decision notes *')
            saved = st.form_submit_button('Record review')
        if saved:
            try:
                add_review(selected_id, reviewer, new_status, decision_notes,
                           security_findings, integration_findings)
            except (ValueError, TypeError) as error:
                st.error(str(error))
            else:
                st.success('Review recorded and status updated.')
                st.rerun()
        st.subheader('Review history')
        history = get_review_history(selected_id)
        if history:
            st.dataframe(history, use_container_width=True, hide_index=True)
        else:
            st.info('No reviews recorded for this request yet.')
