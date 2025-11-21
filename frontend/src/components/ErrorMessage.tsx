interface Props {
message: string;
}


export default function ErrorMessage({ message }: Props) {
return (
<div className="bg-red-100 text-red-700 p-3 rounded-md mb-4">
{message}
</div>
);
}