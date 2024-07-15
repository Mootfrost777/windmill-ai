import Defect from "./Defect.ts";

export default interface Image {
    id: number
    name: string
    filename: string
    defective: string
    uploaded_at: Date
    defects: Defect[]
}