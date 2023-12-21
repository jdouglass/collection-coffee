import UpdatePasswordForm from "@/app/components/UpdatePasswordForm/UpdatePasswordForm";

export default function UpdatePasswordPage({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  return <UpdatePasswordForm searchParams={searchParams} />;
}
