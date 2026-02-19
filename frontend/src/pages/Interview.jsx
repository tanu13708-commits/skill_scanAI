import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { InterviewChat, PageTransition } from '../components'

const Interview = () => {
  const [resumeData, setResumeData] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Get resume data from localStorage
    const storedData = localStorage.getItem('resumeData')
    if (storedData) {
      setResumeData(JSON.parse(storedData))
    }
  }, [])

  const handleInterviewComplete = (result) => {
    // Store interview results and navigate to report
    localStorage.setItem('interviewResult', JSON.stringify(result))
    navigate('/report')
  }

  return (
    <PageTransition>
      <div className="h-[calc(100vh-64px-73px)] flex flex-col">
        {/* Header */}
        <motion.div 
          className="bg-white/5 backdrop-blur-xl border-b border-white/10 px-6 py-4"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <div className="container mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <motion.div 
                  className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/25"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 300 }}
                >
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </motion.div>
                Technical Interview Round
              </h1>
              <p className="text-slate-400 text-sm mt-1 ml-13">Answer questions based on your skills and experience</p>
            </div>
            <motion.div 
              className="flex items-center gap-2"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-sm font-medium backdrop-blur-sm border border-green-500/30">
                Live Session
              </span>
            </motion.div>
          </div>
        </motion.div>

        {/* Chat Area */}
        <motion.div 
          className="flex-1 bg-slate-900/30 backdrop-blur-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="container mx-auto h-full max-w-4xl">
            <div className="bg-white/5 backdrop-blur-xl h-full border-x border-white/10">
              <InterviewChat 
                resumeData={resumeData} 
                onComplete={handleInterviewComplete} 
              />
            </div>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  )
}

export default Interview
