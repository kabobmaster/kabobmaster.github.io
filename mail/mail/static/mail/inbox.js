document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', () => send_mail());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#arc').innerHTML = '';
  document.querySelector('#reply').style.display = 'none';
  
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
    document.querySelector('#reply').style.display = 'block';

        fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // Print email   
              const element = document.querySelector('#email-view');
              element.innerHTML = `<div>From: ${email.sender}</div><div>To: ${email.recipients}</div><h6>Subject: ${email.subject}</h6><div>${email.timestamp}</div><br><div>${email.body}</div>`;
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
                archive = document.querySelector('#arc');
                archive.innerHTML = "<button class='btn btn-sm btn-outline-primary' id='archive'>Archive</button>";

                //mark email archived
              archive.addEventListener('click', function() {
                //mark email as archived
                 fetch(`/emails/${email_id}`, {
                   method: 'PUT',
                   body: JSON.stringify({
                   archived: true
                   })
                   });

                   load_mailbox('inbox');
               });
              }
              if (email.archived == true) {
                unarchive = document.querySelector('#arc');
                unarchive.innerHTML = "<button class='btn btn-sm btn-outline-primary' id='unarchive'>Unarchive</button>";

                unarchive.addEventListener('click', function() {
                  //mark email as unarchived
                   fetch(`/emails/${email_id}`, {
                     method: 'PUT',
                     body: JSON.stringify({
                     archived: false
                     })
                     });
 
                     load_mailbox('inbox');
                 });
              }
              
                 //reply button action
                 reply = document.querySelector('#re');
                 reply.addEventListener('click', function (){
                  compose_email();
                  
                  document.querySelector('#compose-recipients').value = `${email.sender}`;
                  if (email.subject[0]+email.subject[1] == 'Re'){
                    document.querySelector('#compose-subject').value = `${email.subject}`;
                  }
                  else {
                    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
                  }
                  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"`;

                 });

        });

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#arc').innerHTML = '';
  document.querySelector('#reply').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Get emails and list out
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    // Print emails
    emails.forEach(i => {
      const element = document.createElement('div');
      element.innerHTML = `<h6>Sender: ${i.sender}</h6><h6>Subject: ${i.subject}</h6><p>${i.timestamp}</p>`;
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