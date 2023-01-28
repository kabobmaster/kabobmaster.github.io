document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', () => send_mail());
  document.querySelector('#archive').style.display = 'none';
  document.querySelector('#unarchive').style.display = 'none';

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_mail() {

    //Send post email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    
    load_mailbox('sent');
}

function show_email(email_id) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

        fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // Print email   
              const element = document.querySelector('#email-view');
              element.innerHTML = `From: ${email.sender} To: ${email.recipients} Subject: ${email.subject} Timestamp: ${email.timestamp} Body: ${email.body}`;
              element.style.borderStyle = 'outset';
              
            //mark email as read
            fetch(`/emails/${email_id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
              });
              
              //archive button
              user = document.querySelector('#user').value;
              if (user == email.recipients) {
                document.querySelector('#archive').style.display = 'block';
                //doesnt work well, instead either do via HTML or CSS maybe?
              }
        });

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Get emails and list out
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    // Print emails
    emails.forEach(i => {
      const element = document.createElement('div');
      element.innerHTML = `Sender: ${i.sender} Subject: ${i.subject} Timestamp: ${i.timestamp}`;
      element.style.borderStyle = 'outset';
   
      if (i.read == false){
        element.style.backgroundColor = 'grey';
      }

        element.addEventListener('click', function() {
        show_email(i.id);
        });

      document.querySelector('#emails-view').append(element);
      });

    }); 
    
}