import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateEnquiryDto } from './dto/create-enquiry.dto';

@Injectable()
export class EnquiriesService {
  constructor(private readonly prisma: PrismaService) {}

  async create(dto: CreateEnquiryDto) {
    const { website, ...data } = dto;
    if (website) return { accepted: true };

    const enquiry = await this.prisma.enquiry.create({
      data: {
        name: data.name.trim(),
        phone: data.phone.trim(),
        email: data.email?.trim() || null,
        city: data.city.trim(),
        message: data.message.trim(),
        productId: data.productId,
      },
      select: { id: true },
    });

    return { accepted: true, id: enquiry.id };
  }
}
