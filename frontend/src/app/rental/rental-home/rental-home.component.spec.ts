import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RentalHomeComponent } from './rental-home.component';

describe('RentalHomeComponent', () => {
  let component: RentalHomeComponent;
  let fixture: ComponentFixture<RentalHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RentalHomeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RentalHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
