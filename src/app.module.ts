import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { ProductsModule } from './products/products.module';
import { SiteModule } from './site/site.module';

@Module({
  imports: [PrismaModule, ProductsModule, SiteModule],
})
export class AppModule {}
