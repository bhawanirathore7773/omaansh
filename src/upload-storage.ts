import { homedir } from 'os';
import { mkdirSync } from 'fs';
import { join, resolve } from 'path';

/**
 * Persistent media directory for Hostinger production deployments.
 * Override with OSIRA_UPLOADS_DIR if the hosting account has a dedicated persistent path.
 * Default is outside the deployed application tree, under the account's home directory.
 */
export const uploadDirectory = resolve(
  process.env.OSIRA_UPLOADS_DIR || join(process.env.HOME || homedir(), '.osira-uploads'),
);

mkdirSync(uploadDirectory, { recursive: true });
