"""Small command-line demonstration of the request database."""
from database import initialize_database, add_request, get_requests


def main():
    initialize_database()
    if not get_requests():
        request_id = add_request(
            software_name='Analytics Dashboard',
            department='Finance',
            justification='Consolidate monthly reporting.',
            estimated_cost=1200,
            security_notes='Requires role-based access review.',
            integration_notes='May connect to existing reporting data.'
        )
        print(f'Added example request #{request_id}')
    print('\nSoftware requests:')
    for request in get_requests():
        print(f"#{request['id']} | {request['software_name']} | "
              f"{request['department']} | {request['status']} | "
              f"${request['estimated_cost']:.2f}")


if __name__ == '__main__':
    main()
