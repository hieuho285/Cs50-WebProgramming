document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_mail;
  // By default, load the inbox
  load_mailbox('inbox');
});

function send_mail() { 

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject:  document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })  
  })   
  .then(response => response.json())
  .then(result => {
    console.log(result);
  });
  load_mailbox('sent'); 
  return false;
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      mail_box(email, mailbox);
    })    
  });

}
function mail_box(email, mailbox) {
  const border = document.createElement('div');
  border.id = email.id;
  border.classList.add('border', 'border-dark', 'mb-1');

  const row = document.createElement('div');
  row.classList.add('row');

  const sender = document.createElement('strong');
  sender.innerHTML = email.sender;
  sender.classList.add('col-1')

  const subject = document.createElement('div');
  subject.innerHTML = email.subject;
  subject.classList.add('col-6');

  const time = document.createElement('div');
  time.innerHTML = email.timestamp;
  time.classList.add('col-3', 'text-center')

  const archive = document.createElement('div');

  if (mailbox !== 'sent') {
    archive.classList.add('col-2', 'text-center');
    archive.id = "archive";
    if (email.archived === false) {
      archive.innerHTML = 'Archive';
    } else {
      archive.innerHTML = 'Unarchive';
    }
    
  }

  border.appendChild(row)
  row.append(sender, subject, time, archive)

  document.querySelector('#emails-view').append(border);

  if (email.read === false) {
    border.style.background = 'white';
  } else {
    border.style.background = 'gray'; 
  }

  sender.addEventListener('click', () => view_email(email));
  subject.addEventListener('click', () => view_email(email));
  time.addEventListener('click', () => view_email(email));
  archive.addEventListener('click', () => archive_email(email));
}

function view_email(email) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';


  console.log(email);
  read_email(email.id);
  document.querySelector('#email-view-sender').innerHTML = email.sender;
  document.querySelector('#email-view-recipients').innerHTML = email.recipients;
  document.querySelector('#email-view-subject').innerHTML = email.subject;
  document.querySelector('#email-view-time').innerHTML = email.timestamp;
  document.querySelector('#email-view-body').innerHTML = email.body;

  document.querySelector('#reply').addEventListener('click', () => reply_email(email));


}

function reply_email(email) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#title').innerHTML = `Reply to ${email.sender}`
  const comRecipients = document.querySelector('#compose-recipients');
  comRecipients.setAttribute("disabled", true);
  comRecipients.value = email.sender;

  const comSubject = document.querySelector('#compose-subject');
  comSubject.setAttribute("disabled", true);
  if (email.subject.includes("Re:") === true) {
    comSubject.value= email.subject
  } else {
    comSubject.value = `Re: ${email.subject}`
  }

  const comBody = document.querySelector('#compose-body');
  comBody.value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n"${email.body}" `
}

function read_email(email_id) {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  })
}

function archive_email(email) {
  const newValue = !email.archived;
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({     
        archived: newValue
      })
  })
  console.log(email.archived);
  load_mailbox('inbox');
  window.location.reload();
}

