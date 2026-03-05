import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['**/*.vitest.test.ts'],
    reporters: ['default', 'junit'],
    outputFile: {
      junit: './vitest-results/junit.xml',
    },
  },
});
