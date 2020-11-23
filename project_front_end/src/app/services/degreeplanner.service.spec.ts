import { TestBed } from '@angular/core/testing';

import { DegreeplannerService } from './degreeplanner.service';

describe('DegreeplannerService', () => {
  let service: DegreeplannerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DegreeplannerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
