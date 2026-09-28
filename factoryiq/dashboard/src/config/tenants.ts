import type { Tenant } from "../types";
import { pckTenant } from "../services/mockData";

export const tenants: Tenant[] = [
  pckTenant,
];

export const activeTenant = pckTenant;

export function getTenant(tenantId: string): Tenant | undefined {
  return tenants.find((tenant) => tenant.id === tenantId);
}
