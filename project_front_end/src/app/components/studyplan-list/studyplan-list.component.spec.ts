import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyplanListComponent } from './studyplan-list.component';

describe('StudyplanListComponent', () => {
  let component: StudyplanListComponent;
  let fixture: ComponentFixture<StudyplanListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StudyplanListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyplanListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
