import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmitStudyPlanComponent } from './submit-studyplan.component';

describe('SubmitStudyplanComponent', () => {
  let component: SubmitStudyPlanComponent;
  let fixture: ComponentFixture<SubmitStudyPlanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubmitStudyPlanComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmitStudyPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
