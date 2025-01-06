import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-rental',
  standalone: true,
  imports: [RouterModule],
  template: `
    <nav class="subcategories">
      <ul>
        <li><a routerLink="construction" routerLinkActive="active">Maszyny budowlane</a></li>
        <li><a routerLink="garden" routerLinkActive="active">Maszyny ogrodniczo-leśne</a></li>
        <li><a routerLink="trailers" routerLinkActive="active">Przyczepy samochodowe</a></li>
      </ul>
    </nav>
    <router-outlet></router-outlet>
  `,
  styles: [`
    .subcategories {
      background-color: #f0f0f0;
      padding: 10px 0;
    }

    .subcategories ul {
      list-style-type: none;
      padding: 0;
      margin: 0;
      display: flex;
      justify-content: center;
    }

    .subcategories li {
      margin: 0 15px;
    }

    .subcategories a {
      text-decoration: none;
      color: #333;
      font-weight: bold;
    }

    .subcategories a.active {
      color: #007bff;
    }
  `]
})
export class RentalComponent {}
