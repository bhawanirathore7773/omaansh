import { Body, Controller, HttpCode, HttpStatus, Post, Render } from '@nestjs/common';
import { CreateEnquiryDto } from './dto/create-enquiry.dto';
import { EnquiriesService } from './enquiries.service';

@Controller()
export class EnquiriesController {
  constructor(private readonly enquiries: EnquiriesService) {}

  @Post('enquiries')
  @HttpCode(HttpStatus.SEE_OTHER)
  async create(@Body() dto: CreateEnquiryDto) {
    await this.enquiries.create(dto);
    return { ok: true };
  }
}
