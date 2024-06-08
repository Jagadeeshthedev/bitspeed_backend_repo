from flask import request, jsonify, render_template
from src.models.contact_model import Contact
from src import create_app, db
from helper_utils import get_current_time_stamp

app = create_app()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/identify', methods=['POST'])
def identify_contact():
    data = request.json
    phone_number = data.get('phoneNumber')
    email = data.get('email')

    existing_contacts = Contact.query.filter(
        (Contact.phoneNumber == phone_number) | (Contact.email == email)
    ).all()

    if existing_contacts:
        # Finding the primary contact details by oldest date
        primary_contact = min(existing_contacts, key=lambda contact: contact.createdAt)
        if primary_contact.linkPrecedence != 'primary':
            primary_contact.linkPrecedence = 'primary'
            db.session.commit()

        # Checking if the incoming request has new information to the existing contact
        phone_contacts = any(contact.phoneNumber == phone_number for contact in existing_contacts)
        email_contacts = any(contact.email == email for contact in existing_contacts)

        if not (phone_contacts and email_contacts):
            new_contact = Contact(
                phoneNumber=phone_number,
                email=email,
                linkedId=primary_contact.id,
                linkPrecedence='secondary'
            )
            db.session.add(new_contact)
            db.session.commit()
        else:
            # finding the earliest contact by the created timestamp
            newest_contact = max(existing_contacts, key=lambda contact: contact.createdAt)
            if newest_contact.linkPrecedence == 'primary':
                newest_contact.linkedId = primary_contact.id
                newest_contact.linkPrecedence = 'secondary'
                newest_contact.updatedAt = get_current_time_stamp()

    else:
        primary_contact = Contact(
            phoneNumber=phone_number,
            email=email,
            linkPrecedence='primary'
        )
        db.session.add(primary_contact)
        db.session.commit()

    linked_contacts = Contact.query.filter(
        (Contact.linkedId == primary_contact.id) | (Contact.id == primary_contact.id)
    ).all()

    response = {
        'contact': {
            'primaryContactId': primary_contact.id,
            'emails': list(set(contact.email for contact in linked_contacts if contact.email)),
            'phoneNumbers': list(set(contact.phoneNumber for contact in linked_contacts if contact.phoneNumber)),
            'secondaryContactIds': [contact.id for contact in linked_contacts if contact.linkPrecedence == 'secondary']
        }
    }

    return jsonify(response)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(host='0.0.0.0', port=5000)
