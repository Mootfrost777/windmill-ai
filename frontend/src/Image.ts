import Defect from "./Defect.ts";

export default class Image {
    id: number
    name: string
    filename: string
    defective: boolean
    uploaded_at: Date
    defects: Defect[]
}