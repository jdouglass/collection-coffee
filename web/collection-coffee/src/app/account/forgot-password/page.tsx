import ForgotPasswordForm from "@/app/components/ForgotPasswordForm/ForgotPasswordForm";

export default function ForgotPasswordPage({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  return <ForgotPasswordForm searchParams={searchParams} />;
}
