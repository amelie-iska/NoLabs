/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemsModel_Output } from './ItemsModel_Output';
export type PropertyModel_Output = {
    type?: (string | Array<string> | null);
    properties?: (Record<string, PropertyModel_Output> | null);
    required?: Array<string>;
    description?: (string | null);
    enum?: Array<any>;
    const?: null;
    format?: (string | null);
    default?: null;
    example?: null;
    title?: (string | null);
    anyOf?: Array<(PropertyModel_Output | Record<string, any>)>;
    ref?: (string | null);
    items?: (ItemsModel_Output | Array<ItemsModel_Output> | null);
};

