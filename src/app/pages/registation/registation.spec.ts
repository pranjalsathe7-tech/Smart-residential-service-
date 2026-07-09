import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Registation } from './registation';

describe('Registation', () => {
  let component: Registation;
  let fixture: ComponentFixture<Registation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Registation],
    }).compileComponents();

    fixture = TestBed.createComponent(Registation);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
