import ConfigForm from '@/components/config-form';
import CheckForm from '@/components/check-form';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 py-12 px-6 flex justify-center">
      <div className="mx-auto max-w-4xl px-6 w-full flex flex-col gap-10 bg-blue-100">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900">
            Rate Limit Manager
          </h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 items-stretch">
          <ConfigForm />
          <CheckForm />
        </div>

      </div>
    </main>
  );
}
