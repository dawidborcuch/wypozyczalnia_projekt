import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { RentalComponent } from './rental/rental.component';
import {ConstructionMachinesComponent} from './rental/construction-machines/construction-machines.component';
import {GardenMachinesComponent} from './rental/garden-machines/garden-machines.component';
import {TrailersComponent} from './rental/trailers/trailers.component';
import { RentalHomeComponent } from './rental/rental-home/rental-home.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: 'contact', component: ContactComponent },
  {
    path: 'rental',
    component: RentalComponent,
    children: [
      { path: '', component: RentalHomeComponent },
      { path: 'construction', component: ConstructionMachinesComponent },
      { path: 'garden', component: GardenMachinesComponent },
      { path: 'trailers', component: TrailersComponent }
    ]
  },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
