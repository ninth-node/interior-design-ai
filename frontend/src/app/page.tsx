import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          Interior Design AI Platform
        </h1>
        <p className="text-xl text-center mb-12 text-muted-foreground">
          Transform your interior design business with AI-powered design generation,
          3D visualization, and intelligent project management
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-semibold mb-3">AI Design Generation</h2>
            <p className="text-muted-foreground">
              Generate unlimited design concepts with AI-powered creativity
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-semibold mb-3">3D Visualization</h2>
            <p className="text-muted-foreground">
              Photorealistic rendering and AR preview capabilities
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-semibold mb-3">Smart Management</h2>
            <p className="text-muted-foreground">
              Predictive project timelines and resource optimization
            </p>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-muted-foreground">
            Platform Status: Foundation Phase - Core architecture implemented
          </p>
        </div>
      </div>
    </main>
  )
}
