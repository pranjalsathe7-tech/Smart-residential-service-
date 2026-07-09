import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Availbal } from './availbal';

describe('Availbal', () => {
  let component: Availbal;
  let fixture: ComponentFixture<Availbal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Availbal],
    }).compileComponents();

    fixture = TestBed.createComponent(Availbal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
