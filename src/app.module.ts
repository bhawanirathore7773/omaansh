import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { ProductsModule } from './products/products.module';
import { CategoriesModule } from './categories/categories.module';
import { ServicesModule } from './services/services.module';
import { IndustriesModule } from './industries/industries.module';
import { CitiesModule } from './cities/cities.module';
import { BlogModule } from './blog/blog.module';
import { EnquiriesModule } from './enquiries/enquiries.module';
import { SiteModule } from './site/site.module';
import { AdminModule } from './admin/admin.module';

@Module({
  imports: [PrismaModule, ProductsModule, CategoriesModule, ServicesModule, IndustriesModule, CitiesModule, BlogModule, EnquiriesModule, SiteModule, AdminModule],
})
export class AppModule {}
