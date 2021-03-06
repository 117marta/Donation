document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit  --> skomentowa?? to!
      // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }


  // STEP 3 - nie dzia??a!!!!
  let checked_categories = []
  // let categories_of_institution = []
  const categories_checkbox = document.querySelectorAll('input[name="categories"]');
  const categories = document.querySelectorAll('input[name="category"]')
  const divs = document.querySelectorAll('#step3')
  categories_checkbox.forEach(function (el){
    el.addEventListener('change', function (event){
      if(this.checked){
        checked_categories.push(el.value)
        console.log("Zaznaczone")
        console.log(checked_categories)
          categories.forEach(function (el){
            if(checked_categories.includes(el.value)){
              // categories_of_institution.push(el.value)
              console.log("PR??BA")
              el.parentElement.parentElement.style.display = "block";
            }
            // else{
            //   el.parentElement.parentElement.style.display = "none";
            // }
          })
      }
      else if(this.checked == false){
        checked_categories.splice(checked_categories.indexOf(el))
        console.log(checked_categories)
      }
    })
  })


  // STEP 4 - nie dzia??a!!!!
  const number_of_bags = document.querySelector('input[name="bags"]')
  const summary_text = document.querySelector('#summary-details')
  const summary_institution = document.querySelector('#summary-institution')
  const summary_trigger = document.querySelector('#summaryTrigger')
  const organizations = document.querySelectorAll('input[name="organization"]')

  const street = document.querySelector('input[name="address"]')
  const city = document.querySelector('input[name="city"]')
  const postcode = document.querySelector('input[name="zip_code"]')
  const phone = document.querySelector('input[name="phone"]')

  const pick_up_date = document.querySelector('input[name="pick_up_date"]')
  const pick_up_time = document.querySelector('input[name="pick_up_time"]')
  const pick_up_comment = document.querySelector('textarea[name="pick_up_comment"]')

  let checked_categories_names = []
  const categories_checkbox_names = document.querySelectorAll('input[name="categories"]');
  categories_checkbox_names.forEach(function (el){
  el.addEventListener('change', function (event){
    if(this.checked) {
      checked_categories_names.push(el.id)
    }})})

  summary_trigger.addEventListener('click', function (){
    // summary_text.innerText = number_of_bags.value+" worki zawieraj??ce: " + checked_categories_names
  if (number_of_bags.value == 1) {
    summary_text.innerText = 'Oddajesz ' + number_of_bags.value + ' worek zawieraj??cy: ' + checked_categories_names
  } else if (number_of_bags.value == 2) {
    summary_text.innerText = 'Oddajesz ' + number_of_bags.value + ' worki zawieraj??ce: ' + checked_categories_names
  } else if (number_of_bags.value == 3) {
    summary_text.innerText = 'Oddajesz ' + number_of_bags.value + ' worki zawieraj??ce: ' + checked_categories_names
  } else if (number_of_bags.value == 4) {
    summary_text.innerText = 'Oddajesz ' + number_of_bags.value + ' worki zawieraj??ce: ' + checked_categories_names
  } else {
    summary_text.innerText = 'Oddajesz ' + number_of_bags.value + ' work??w zawieraj??cych: ' + checked_categories_names
  }
    document.querySelector('input[name="checked_categories_backend"]').value = checked_categories
    organizations.forEach(function (organization){
      if(organization.checked){
        summary_institution.innerText = 'Dla fundacji "'+organization.value+'"'
      }
    })
    document.querySelector('#street').innerText = street.value
    document.querySelector('#city').innerText = city.value
    document.querySelector('#zip_code').innerText = postcode.value
    document.querySelector('#phone').innerText = phone.value

    document.querySelector('#pick_up_date').innerText = pick_up_date.value
    document.querySelector('#pick_up_time').innerText = pick_up_time.value
    document.querySelector('#pick_up_comment').innerText = pick_up_comment.value
  })

});
