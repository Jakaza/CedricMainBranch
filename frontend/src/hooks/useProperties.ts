import { useQuery } from '@tanstack/react-query';
import { propertyService } from '@/services/propertyService';

// Query keys
export const propertyKeys = {
    all: ['properties'] as const,
    lists: () => [...propertyKeys.all, 'list'] as const,
    list: (category?: string) => [...propertyKeys.lists(), category] as const,
    details: () => [...propertyKeys.all, 'detail'] as const,
    detail: (id: string) => [...propertyKeys.details(), id] as const,
};

// Get all properties
export const useProperties = () => {
    return useQuery({
        queryKey: propertyKeys.lists(),
        queryFn: () => propertyService.getAll(),
    });
};

// Get single property by ID
export const useProperty = (id: string) => {
    return useQuery({
        queryKey: propertyKeys.detail(id),
        queryFn: () => propertyService.getById(id),
        enabled: !!id,
    });
};

// Get house plans only
export const useHousePlans = () => {
    return useQuery({
        queryKey: propertyKeys.list('plans'),
        queryFn: () => propertyService.getPlans(),
    });
};

// Get built homes only
export const useBuiltHomes = () => {
    return useQuery({
        queryKey: propertyKeys.list('built'),
        queryFn: () => propertyService.getBuilt(),
    });
};
