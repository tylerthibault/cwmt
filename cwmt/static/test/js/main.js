document.addEventListener('DOMContentLoaded', function() {
    // Set dark mode based on saved preference in localStorage
    if (localStorage.getItem('darkMode') === 'true') {
      document.body.classList.add('dark-mode');
    }
  
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
      darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const icon = this.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
          icon.classList.remove('fa-moon');
          icon.classList.add('fa-sun');
          localStorage.setItem('darkMode', 'true');
        } else {
          icon.classList.remove('fa-sun');
          icon.classList.add('fa-moon');
          localStorage.setItem('darkMode', 'false');
        }
      });
    }
  
    // FAQ Toggle Functionality
    const faqHeaders = document.querySelectorAll('.faq-item h4');
    faqHeaders.forEach(function(header) {
      header.addEventListener('click', function() {
        this.parentElement.classList.toggle('active');
      });
    });
  
    // Initialize FullCalendar if the #calendar element exists (for calendar & signup page)
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
      var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [
          {
            title: 'Beginner Riding Course',
            start: '2025-02-05T10:00:00',
            end: '2025-02-05T12:00:00',
            color: '#ff5a5f'
          },
          {
            title: 'Advanced Techniques',
            start: '2025-02-10T14:00:00',
            end: '2025-02-10T16:00:00',
            color: '#e04e52'
          },
          {
            title: 'Safety Workshops',
            start: '2025-02-15T09:00:00',
            end: '2025-02-15T11:00:00',
            color: '#ff5a5f'
          },
          {
            title: 'Weekend Riding Basics',
            start: '2025-02-20T08:00:00',
            end: '2025-02-20T12:00:00',
            color: '#e04e52'
          },
          {
            title: 'Advanced Road Skills',
            start: '2025-02-22T13:00:00',
            end: '2025-02-22T15:00:00',
            color: '#ff5a5f'
          },
          {
            title: 'Night Riding Techniques',
            start: '2025-02-25T19:00:00',
            end: '2025-02-25T21:00:00',
            color: '#e04e52'
          }
        ]
      });
      calendar.render();
    }
  
    // Signup Form Submission (dummy submission)
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
      signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for signing up! We will contact you soon.');
        signupForm.reset();
      });
    }
  });
  