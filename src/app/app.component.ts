import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'muradHotels';

  formData = {
    name: '',
    email: '',
    phone: '',
    buy: false,
    sell: false,
    currentPlan: ''
  };

  showCheckboxes = true;
  showCurrentPlan = false;

  constructor(private http: HttpClient) { }

  bookNowForm(pricingPlan: string, pricingSum: string) {
    this.formData.currentPlan = `${pricingPlan} - ${pricingSum}`;
    this.showCurrentPlan = true;
    this.showCheckboxes = false;
  }

  bookAppointmentForm() {
    this.formData.currentPlan = '';
    this.showCurrentPlan = false;
    this.showCheckboxes = true;
  }

  onSubmit() {
    const payload = {
      name: this.formData.name,
      email: this.formData.email,
      phone: this.formData.phone,
      buy: this.formData.buy,
      sell: this.formData.sell,
      currentPlan: this.formData.currentPlan || null
    };

    this.http.post('http://localhost:8000/send-email', payload).subscribe({
      next: () => alert('Email sent successfully'),
      error: () => alert('Error sending email')
    });
  }

  clearForm() {
    this.formData = {
      name: '',
      email: '',
      phone: '',
      buy: false,
      sell: false,
      currentPlan: ''
    };
    this.showCurrentPlan = false;
    this.showCheckboxes = true;
  }
}
