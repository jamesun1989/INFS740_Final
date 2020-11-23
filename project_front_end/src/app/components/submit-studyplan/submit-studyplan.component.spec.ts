import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmitStudyplanComponent } from './submit-studyplan.component';

describe('SubmitStudyplanComponent', () => {
  let component: SubmitStudyplanComponent;
  let fixture: ComponentFixture<SubmitStudyplanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubmitStudyplanComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmitStudyplanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
