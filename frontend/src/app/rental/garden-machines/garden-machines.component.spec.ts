import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GardenMachinesComponent } from './garden-machines.component';

describe('GardenMachinesComponent', () => {
  let component: GardenMachinesComponent;
  let fixture: ComponentFixture<GardenMachinesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GardenMachinesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GardenMachinesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
