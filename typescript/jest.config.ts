import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/tests/jest/**/*.test.ts'],
  reporters: ['default'],
};

export default config;
